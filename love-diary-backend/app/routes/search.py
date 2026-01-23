from flask import Blueprint, request, jsonify
from app.models import Photo, Video, Diary

search_bp = Blueprint('search', __name__)

@search_bp.route('', methods=['GET'])
def search():
    """搜索内容"""
    try:
        keyword = request.args.get('keyword', '').strip()
        content_type = request.args.get('type', 'all')  # all, photos, videos, diaries
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        results = {
            'photos': [],
            'videos': [],
            'diaries': [],
            'total': 0
        }

        if not keyword:
            return jsonify(results)

        # 搜索照片
        if content_type in ['all', 'photos']:
            photos = Photo.query.filter(
                (Photo.title.like(f'%{keyword}%')) |
                (Photo.description.like(f'%{keyword}%')) |
                (Photo.tags.like(f'%{keyword}%')) |
                (Photo.category.like(f'%{keyword}%'))
            ).order_by(Photo.created_at.desc()).limit(per_page).all()

            results['photos'] = [photo.to_dict() for photo in photos]

        # 搜索视频
        if content_type in ['all', 'videos']:
            videos = Video.query.filter(
                (Video.title.like(f'%{keyword}%')) |
                (Video.description.like(f'%{keyword}%')) |
                (Video.tags.like(f'%{keyword}%')) |
                (Video.category.like(f'%{keyword}%'))
            ).order_by(Video.created_at.desc()).limit(per_page).all()

            results['videos'] = [video.to_dict() for video in videos]

        # 搜索日记
        if content_type in ['all', 'diaries']:
            diaries = Diary.query.filter(
                (Diary.title.like(f'%{keyword}%')) |
                (Diary.content.like(f'%{keyword}%')) |
                (Diary.tags.like(f'%{keyword}%')) |
                (Diary.category.like(f'%{keyword}%')) |
                (Diary.mood.like(f'%{keyword}%'))
            ).order_by(Diary.created_at.desc()).limit(per_page).all()

            results['diaries'] = [diary.to_dict() for diary in diaries]

        results['total'] = len(results['photos']) + len(results['videos']) + len(results['diaries'])

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': '搜索失败'}), 500