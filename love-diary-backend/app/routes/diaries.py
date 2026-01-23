from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.models import Diary, db
from app.utils.decorators import admin_required

diaries_bp = Blueprint('diaries', __name__)

@diaries_bp.route('', methods=['GET'])
def get_diaries():
    """获取日记列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        tags = request.args.get('tags')
        mood = request.args.get('mood')

        query = Diary.query

        # 分类筛选
        if category:
            query = query.filter(Diary.category == category)

        # 标签筛选
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                query = query.filter(Diary.tags.like(f'%{tag}%'))

        # 心情筛选
        if mood:
            query = query.filter(Diary.mood == mood)

        # 分页
        diaries = query.order_by(Diary.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'diaries': [diary.to_dict() for diary in diaries.items],
            'total': diaries.total,
            'page': page,
            'per_page': per_page,
            'pages': diaries.pages
        })

    except Exception as e:
        return jsonify({'error': '获取日记列表失败'}), 500

@diaries_bp.route('', methods=['POST'])
@login_required
@admin_required
def create_diary():
    """创建日记"""
    try:
        data = request.get_json()

        if not data or not data.get('title') or not data.get('content'):
            return jsonify({'error': '标题和内容不能为空'}), 400

        # 创建日记
        diary = Diary(
            user_id=current_user.id,
            title=data.get('title'),
            content=data.get('content'),
            category=data.get('category', '日常'),
            tags=','.join([tag.strip() for tag in data.get('tags', []) if tag.strip()]),
            mood=data.get('mood')
        )

        db.session.add(diary)
        db.session.commit()

        return jsonify({
            'message': '日记创建成功',
            'diary': diary.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '日记创建失败'}), 500

@diaries_bp.route('/<int:diary_id>', methods=['GET'])
def get_diary(diary_id):
    """获取单篇日记"""
    try:
        diary = Diary.query.get_or_404(diary_id)
        return jsonify(diary.to_dict())
    except Exception as e:
        return jsonify({'error': '获取日记详情失败'}), 500

@diaries_bp.route('/<int:diary_id>', methods=['PUT'])
@login_required
@admin_required
def update_diary(diary_id):
    """更新日记"""
    try:
        diary = Diary.query.get_or_404(diary_id)
        data = request.get_json()

        # 更新字段
        if 'title' in data:
            diary.title = data['title']
        if 'content' in data:
            diary.content = data['content']
        if 'category' in data:
            diary.category = data['category']
        if 'tags' in data:
            tags_list = data['tags'] if isinstance(data['tags'], list) else data['tags'].split(',')
            diary.tags = ','.join([tag.strip() for tag in tags_list if tag.strip()])
        if 'mood' in data:
            diary.mood = data['mood']

        db.session.commit()

        return jsonify({
            'message': '日记更新成功',
            'diary': diary.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '日记更新失败'}), 500

@diaries_bp.route('/<int:diary_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_diary(diary_id):
    """删除日记"""
    try:
        diary = Diary.query.get_or_404(diary_id)

        db.session.delete(diary)
        db.session.commit()

        return jsonify({'message': '日记删除成功'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '日记删除失败'}), 500

@diaries_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有日记分类"""
    try:
        categories = db.session.query(Diary.category).distinct().all()
        category_list = [cat[0] for cat in categories if cat[0]]
        return jsonify({'categories': category_list})
    except Exception as e:
        return jsonify({'error': '获取分类失败'}), 500

@diaries_bp.route('/tags', methods=['GET'])
def get_tags():
    """获取所有日记标签"""
    try:
        diaries = Diary.query.filter(Diary.tags != '').all()
        all_tags = set()
        for diary in diaries:
            if diary.tags:
                tags = [tag.strip() for tag in diary.tags.split(',') if tag.strip()]
                all_tags.update(tags)
        return jsonify({'tags': list(all_tags)})
    except Exception as e:
        return jsonify({'error': '获取标签失败'}), 500

@diaries_bp.route('/moods', methods=['GET'])
def get_moods():
    """获取所有心情类型"""
    try:
        moods = db.session.query(Diary.mood).distinct().filter(Diary.mood.isnot(None)).all()
        mood_list = [mood[0] for mood in moods if mood[0]]
        return jsonify({'moods': mood_list})
    except Exception as e:
        return jsonify({'error': '获取心情类型失败'}), 500