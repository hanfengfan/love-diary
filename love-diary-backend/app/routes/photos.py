import os
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
from app.models import Photo, db
from app.utils.decorators import admin_required
from app.utils.file import save_uploaded_file

photos_bp = Blueprint('photos', __name__)

@photos_bp.route('', methods=['GET'])
def get_photos():
    """获取照片列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        tags = request.args.get('tags')

        query = Photo.query

        # 分类筛选
        if category:
            query = query.filter(Photo.category == category)

        # 标签筛选
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                query = query.filter(Photo.tags.like(f'%{tag}%'))

        # 分页
        photos = query.order_by(Photo.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'photos': [photo.to_dict() for photo in photos.items],
            'total': photos.total,
            'page': page,
            'per_page': per_page,
            'pages': photos.pages
        })

    except Exception as e:
        return jsonify({'error': '获取照片列表失败'}), 500

@photos_bp.route('', methods=['POST'])
@login_required
@admin_required
def upload_photo():
    """上传照片"""
    try:
        if 'photo' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400

        file = request.files['photo']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400

        # 获取表单数据
        title = request.form.get('title', '未命名照片')
        description = request.form.get('description', '')
        category = request.form.get('category', '日常')
        tags = request.form.get('tags', '')

        # 保存文件
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos')
        filename, error = save_uploaded_file(
            file, upload_folder, current_app.config['ALLOWED_PHOTO_EXTENSIONS']
        )

        if error:
            return jsonify({'error': error}), 400

        # 创建照片记录
        photo = Photo(
            user_id=current_user.id,
            title=title,
            description=description,
            filename=filename,
            filepath=os.path.join('photos', filename),
            category=category,
            tags=','.join([tag.strip() for tag in tags.split(',') if tag.strip()])
        )

        db.session.add(photo)
        db.session.commit()

        return jsonify({
            'message': '照片上传成功',
            'photo': photo.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '照片上传失败'}), 500

@photos_bp.route('/<int:photo_id>', methods=['GET'])
def get_photo(photo_id):
    """获取单张照片详情"""
    try:
        photo = Photo.query.get_or_404(photo_id)
        return jsonify(photo.to_dict())
    except Exception as e:
        return jsonify({'error': '获取照片详情失败'}), 500

@photos_bp.route('/<int:photo_id>', methods=['PUT'])
@login_required
@admin_required
def update_photo(photo_id):
    """更新照片信息"""
    try:
        photo = Photo.query.get_or_404(photo_id)
        data = request.get_json()

        # 更新字段
        if 'title' in data:
            photo.title = data['title']
        if 'description' in data:
            photo.description = data['description']
        if 'category' in data:
            photo.category = data['category']
        if 'tags' in data:
            tags_list = data['tags'] if isinstance(data['tags'], list) else data['tags'].split(',')
            photo.tags = ','.join([tag.strip() for tag in tags_list if tag.strip()])

        db.session.commit()

        return jsonify({
            'message': '照片信息更新成功',
            'photo': photo.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '照片信息更新失败'}), 500

@photos_bp.route('/<int:photo_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_photo(photo_id):
    """删除照片"""
    try:
        photo = Photo.query.get_or_404(photo_id)

        # 删除文件
        photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filepath)
        if os.path.exists(photo_path):
            os.remove(photo_path)

        # 删除数据库记录
        db.session.delete(photo)
        db.session.commit()

        return jsonify({'message': '照片删除成功'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '照片删除失败'}), 500

@photos_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有照片分类"""
    try:
        categories = db.session.query(Photo.category).distinct().all()
        category_list = [cat[0] for cat in categories if cat[0]]
        return jsonify({'categories': category_list})
    except Exception as e:
        return jsonify({'error': '获取分类失败'}), 500

@photos_bp.route('/tags', methods=['GET'])
def get_tags():
    """获取所有照片标签"""
    try:
        photos = Photo.query.filter(Photo.tags != '').all()
        all_tags = set()
        for photo in photos:
            if photo.tags:
                tags = [tag.strip() for tag in photo.tags.split(',') if tag.strip()]
                all_tags.update(tags)
        return jsonify({'tags': list(all_tags)})
    except Exception as e:
        return jsonify({'error': '获取标签失败'}), 500