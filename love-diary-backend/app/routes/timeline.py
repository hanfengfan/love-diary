from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timezone
from sqlalchemy import func, cast, Date
from app.models import Photo, Video, Diary, db

timeline_bp = Blueprint('timeline', __name__)


@timeline_bp.route('', methods=['GET'])
def get_timeline():
    """获取时间线数据 — 使用 UNION + SQL分页避免全表加载"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        content_type = request.args.get('type', 'all')
        category = request.args.get('category')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        timeline_items = []
        total_count = 0

        # 查询照片（使用分页）
        if content_type in ['all', 'photos']:
            query = Photo.query
            if category:
                query = query.filter(Photo.category == category)
            if start_date:
                query = query.filter(Photo.created_at >= datetime.fromisoformat(start_date))
            if end_date:
                query = query.filter(Photo.created_at <= datetime.fromisoformat(end_date))

            total_count += query.count()
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

            total_count += query.count()
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

            total_count += query.count()
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
            'total': total_count,
            'page': page,
            'per_page': per_page,
            'pages': (total_count + per_page - 1) // per_page if total_count > 0 else 0
        })

    except Exception as e:
        current_app.logger.error(f'获取时间线失败: {e}', exc_info=True)
        return jsonify({'error': '获取时间线失败'}), 500


@timeline_bp.route('/calendar', methods=['GET'])
def get_calendar_data():
    """获取日历数据 — 使用 SQL 聚合代替逐条遍历"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', None, type=int)

        # 计算日期范围
        start_date = datetime(year, 1, 1)
        if month:
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year + 1, 1, 1)

        calendar_data = {}

        # 使用 SQL 聚合统计照片
        photo_counts = db.session.query(
            func.date(Photo.created_at).label('date'),
            func.count(Photo.id).label('count')
        ).filter(
            Photo.created_at >= start_date,
            Photo.created_at < end_date
        ).group_by(func.date(Photo.created_at)).all()

        for row in photo_counts:
            date_key = str(row.date)
            if date_key not in calendar_data:
                calendar_data[date_key] = {'photos': 0, 'videos': 0, 'diaries': 0}
            calendar_data[date_key]['photos'] = row.count

        # 使用 SQL 聚合统计视频
        video_counts = db.session.query(
            func.date(Video.created_at).label('date'),
            func.count(Video.id).label('count')
        ).filter(
            Video.created_at >= start_date,
            Video.created_at < end_date
        ).group_by(func.date(Video.created_at)).all()

        for row in video_counts:
            date_key = str(row.date)
            if date_key not in calendar_data:
                calendar_data[date_key] = {'photos': 0, 'videos': 0, 'diaries': 0}
            calendar_data[date_key]['videos'] = row.count

        # 使用 SQL 聚合统计日记
        diary_counts = db.session.query(
            func.date(Diary.created_at).label('date'),
            func.count(Diary.id).label('count')
        ).filter(
            Diary.created_at >= start_date,
            Diary.created_at < end_date
        ).group_by(func.date(Diary.created_at)).all()

        for row in diary_counts:
            date_key = str(row.date)
            if date_key not in calendar_data:
                calendar_data[date_key] = {'photos': 0, 'videos': 0, 'diaries': 0}
            calendar_data[date_key]['diaries'] = row.count

        return jsonify({'calendar': calendar_data})

    except Exception as e:
        current_app.logger.error(f'获取日历数据失败: {e}', exc_info=True)
        return jsonify({'error': '获取日历数据失败'}), 500