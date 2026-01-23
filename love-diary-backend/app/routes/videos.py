import os
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
from app.models import Video, db
from app.utils.decorators import admin_required
from app.utils.file import save_uploaded_file, generate_video_thumbnail, get_video_duration

videos_bp = Blueprint('videos', __name__)

@videos_bp.route('', methods=['GET'])
def get_videos():
    """获取视频列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        tags = request.args.get('tags')

        query = Video.query

        # 分类筛选
        if category:
            query = query.filter(Video.category == category)

        # 标签筛选
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                query = query.filter(Video.tags.like(f'%{tag}%'))

        # 分页
        videos = query.order_by(Video.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'videos': [video.to_dict() for video in videos.items],
            'total': videos.total,
            'page': page,
            'per_page': per_page,
            'pages': videos.pages
        })

    except Exception as e:
        return jsonify({'error': '获取视频列表失败'}), 500

@videos_bp.route('', methods=['POST'])
@login_required
@admin_required
def upload_video():
    """上传视频"""
    try:
        if 'video' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400

        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400

        # 获取表单数据
        title = request.form.get('title', '未命名视频')
        description = request.form.get('description', '')
        category = request.form.get('category', '日常')
        tags = request.form.get('tags', '')

        # 保存视频文件
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'videos')
        filename, error = save_uploaded_file(
            file, upload_folder, current_app.config['ALLOWED_VIDEO_EXTENSIONS']
        )

        if error:
            return jsonify({'error': error}), 400

        video_path = os.path.join(upload_folder, filename)

        # 生成缩略图
        thumbnail_filename = None
        thumbnail_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'], 'thumbnails',
            f'thumb_{filename.split(".")[0]}.jpg'
        )
        os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

        if generate_video_thumbnail(video_path, thumbnail_path):
            thumbnail_filename = os.path.join('thumbnails', f'thumb_{filename.split(".")[0]}.jpg')

        # 获取视频时长
        duration = get_video_duration(video_path)

        # 创建视频记录
        video = Video(
            user_id=current_user.id,
            title=title,
            description=description,
            filename=filename,
            filepath=os.path.join('videos', filename),
            thumbnail=thumbnail_filename,
            category=category,
            tags=','.join([tag.strip() for tag in tags.split(',') if tag.strip()]),
            duration=duration
        )

        db.session.add(video)
        db.session.commit()

        return jsonify({
            'message': '视频上传成功',
            'video': video.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '视频上传失败'}), 500

@videos_bp.route('/<int:video_id>', methods=['GET'])
def get_video(video_id):
    """获取单个视频详情"""
    try:
        video = Video.query.get_or_404(video_id)
        return jsonify(video.to_dict())
    except Exception as e:
        return jsonify({'error': '获取视频详情失败'}), 500

@videos_bp.route('/<int:video_id>', methods=['PUT'])
@login_required
@admin_required
def update_video(video_id):
    """更新视频信息"""
    try:
        video = Video.query.get_or_404(video_id)
        data = request.get_json()

        # 更新字段
        if 'title' in data:
            video.title = data['title']
        if 'description' in data:
            video.description = data['description']
        if 'category' in data:
            video.category = data['category']
        if 'tags' in data:
            tags_list = data['tags'] if isinstance(data['tags'], list) else data['tags'].split(',')
            video.tags = ','.join([tag.strip() for tag in tags_list if tag.strip()])

        db.session.commit()

        return jsonify({
            'message': '视频信息更新成功',
            'video': video.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '视频信息更新失败'}), 500

@videos_bp.route('/<int:video_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_video(video_id):
    """删除视频"""
    try:
        video = Video.query.get_or_404(video_id)

        # 删除视频文件
        video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], video.filepath)
        if os.path.exists(video_path):
            os.remove(video_path)

        # 删除缩略图
        if video.thumbnail:
            thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], video.thumbnail)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)

        # 删除数据库记录
        db.session.delete(video)
        db.session.commit()

        return jsonify({'message': '视频删除成功'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '视频删除失败'}), 500

@videos_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有视频分类"""
    try:
        categories = db.session.query(Video.category).distinct().all()
        category_list = [cat[0] for cat in categories if cat[0]]
        return jsonify({'categories': category_list})
    except Exception as e:
        return jsonify({'error': '获取分类失败'}), 500

@videos_bp.route('/tags', methods=['GET'])
def get_tags():
    """获取所有视频标签"""
    try:
        videos = Video.query.filter(Video.tags != '').all()
        all_tags = set()
        for video in videos:
            if video.tags:
                tags = [tag.strip() for tag in video.tags.split(',') if tag.strip()]
                all_tags.update(tags)
        return jsonify({'tags': list(all_tags)})
    except Exception as e:
        return jsonify({'error': '获取标签失败'}), 500