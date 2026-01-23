from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy import or_
from app.models import Photo, Video, Diary

timeline_bp = Blueprint('timeline', __name__)

@timeline_bp.route('', methods=['GET'])
def get_timeline():
    """获取时间线数据"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        content_type = request.args.get('type', 'all')  # all, photos, videos, diaries
        category = request.args.get('category')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        timeline_items = []

        # 查询照片
        if content_type in ['all', 'photos']:
            query = Photo.query
            if category:
                query = query.filter(Photo.category == category)
            if start_date:
                query = query.filter(Photo.created_at >= datetime.fromisoformat(start_date))
            if end_date:
                query = query.filter(Photo.created_at <= datetime.fromisoformat(end_date))

            photos = query.order_by(Photo.created_at.desc()).all()
            for photo in photos:
                timeline_items.append({
                    'id': photo.id,
                    'type': 'photo',
                    'title': photo.title,
                    'description': photo.description,
                    'filepath': photo.filepath,
                    'category': photo.category,
                    'tags': photo.tags.split(',') if photo.tags else [],
                    'created_at': photo.created_at.isoformat(),
                    'data': photo.to_dict()
                })

        # 查询视频
        if content_type in ['all', 'videos']:
            query = Video.query
            if category:
                query = query.filter(Video.category == category)
            if start_date:
                query = query.filter(Video.created_at >= datetime.fromisoformat(start_date))
            if end_date:
                query = query.filter(Video.created_at <= datetime.fromisoformat(end_date))

            videos = query.order_by(Video.created_at.desc()).all()
            for video in videos:
                timeline_items.append({
                    'id': video.id,
                    'type': 'video',
                    'title': video.title,
                    'description': video.description,
                    'filepath': video.filepath,
                    'thumbnail': video.thumbnail,
                    'category': video.category,
                    'tags': video.tags.split(',') if video.tags else [],
                    'duration': video.duration,
                    'created_at': video.created_at.isoformat(),
                    'data': video.to_dict()
                })

        # 查询日记
        if content_type in ['all', 'diaries']:
            query = Diary.query
            if category:
                query = query.filter(Diary.category == category)
            if start_date:
                query = query.filter(Diary.created_at >= datetime.fromisoformat(start_date))
            if end_date:
                query = query.filter(Diary.created_at <= datetime.fromisoformat(end_date))

            diaries = query.order_by(Diary.created_at.desc()).all()
            for diary in diaries:
                timeline_items.append({
                    'id': diary.id,
                    'type': 'diary',
                    'title': diary.title,
                    'content': diary.content,
                    'category': diary.category,
                    'tags': diary.tags.split(',') if diary.tags else [],
                    'mood': diary.mood,
                    'created_at': diary.created_at.isoformat(),
                    'data': diary.to_dict()
                })

        # 按时间排序
        timeline_items.sort(key=lambda x: x['created_at'], reverse=True)

        # 分页
        start = (page - 1) * per_page
        end = start + per_page
        paginated_items = timeline_items[start:end]

        return jsonify({
            'timeline': paginated_items,
            'total': len(timeline_items),
            'page': page,
            'per_page': per_page,
            'pages': (len(timeline_items) + per_page - 1) // per_page
        })

    except Exception as e:
        return jsonify({'error': '获取时间线失败'}), 500

@timeline_bp.route('/calendar', methods=['GET'])
def get_calendar_data():
    """获取日历数据（按日期统计内容数量）"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', None, type=int)

        calendar_data = {}

        # 查询指定年月的数据
        start_date = datetime(year, 1, 1)
        if month:
            end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            start_date = datetime(year, month, 1)
        else:
            end_date = datetime(year + 1, 1, 1)

        # 统计照片
        photos = Photo.query.filter(
            Photo.created_at >= start_date,
            Photo.created_at < end_date
        ).all()

        for photo in photos:
            date_key = photo.created_at.strftime('%Y-%m-%d')
            if date_key not in calendar_data:
                calendar_data[date_key] = {'photos': 0, 'videos': 0, 'diaries': 0}
            calendar_data[date_key]['photos'] += 1

        # 统计视频
        videos = Video.query.filter(
            Video.created_at >= start_date,
            Video.created_at < end_date
        ).all()

        for video in videos:
            date_key = video.created_at.strftime('%Y-%m-%d')
            if date_key not in calendar_data:
                calendar_data[date_key] = {'photos': 0, 'videos': 0, 'diaries': 0}
            calendar_data[date_key]['videos'] += 1

        # 统计日记
        diaries = Diary.query.filter(
            Diary.created_at >= start_date,
            Diary.created_at < end_date
        ).all()

        for diary in diaries:
            date_key = diary.created_at.strftime('%Y-%m-%d')
            if date_key not in calendar_data:
                calendar_data[date_key] = {'photos': 0, 'videos': 0, 'diaries': 0}
            calendar_data[date_key]['diaries'] += 1

        return jsonify({'calendar': calendar_data})

    except Exception as e:
        return jsonify({'error': '获取日历数据失败'}), 500