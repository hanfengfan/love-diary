from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from app.models import Photo, Video, Diary, db
from flask_login import login_required
from app.utils.decorators import admin_required

statistics_bp = Blueprint('statistics', __name__)


@statistics_bp.route('', methods=['GET'])
@login_required
@admin_required
def get_statistics():
    """获取统计数据"""
    try:
        # 基础统计
        photo_count = Photo.query.count()
        video_count = Video.query.count()
        diary_count = Diary.query.count()

        # 分类统计
        photo_categories = Photo.query.with_entities(
            Photo.category, func.count(Photo.id)
        ).group_by(Photo.category).all()

        video_categories = Video.query.with_entities(
            Video.category, func.count(Video.id)
        ).group_by(Video.category).all()

        diary_categories = Diary.query.with_entities(
            Diary.category, func.count(Diary.id)
        ).group_by(Diary.category).all()

        # 心情统计
        diary_moods = Diary.query.with_entities(
            Diary.mood, func.count(Diary.id)
        ).filter(Diary.mood.isnot(None)).group_by(Diary.mood).all()

        # 最近7天的数据统计
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

        recent_photos = Photo.query.filter(Photo.created_at >= seven_days_ago).count()
        recent_videos = Video.query.filter(Video.created_at >= seven_days_ago).count()
        recent_diaries = Diary.query.filter(Diary.created_at >= seven_days_ago).count()

        # 最近30天的数据统计
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

        monthly_photos = Photo.query.filter(Photo.created_at >= thirty_days_ago).count()
        monthly_videos = Video.query.filter(Video.created_at >= thirty_days_ago).count()
        monthly_diaries = Diary.query.filter(Diary.created_at >= thirty_days_ago).count()

        # 总存储统计
        total_storage = photo_count + video_count + diary_count

        return jsonify({
            'basic_stats': {
                'total_photos': photo_count,
                'total_videos': video_count,
                'total_diaries': diary_count,
                'total_storage': total_storage
            },
            'category_stats': {
                'photos': [{'category': cat, 'count': count} for cat, count in photo_categories],
                'videos': [{'category': cat, 'count': count} for cat, count in video_categories],
                'diaries': [{'category': cat, 'count': count} for cat, count in diary_categories]
            },
            'mood_stats': [{'mood': mood, 'count': count} for mood, count in diary_moods],
            'recent_stats': {
                'last_7_days': {
                    'photos': recent_photos,
                    'videos': recent_videos,
                    'diaries': recent_diaries
                },
                'last_30_days': {
                    'photos': monthly_photos,
                    'videos': monthly_videos,
                    'diaries': monthly_diaries
                }
            }
        })

    except Exception as e:
        current_app.logger.error(f'获取统计数据失败: {e}', exc_info=True)
        return jsonify({'error': '获取统计数据失败'}), 500


@statistics_bp.route('/timeline', methods=['GET'])
@login_required
@admin_required
def get_timeline_statistics():
    """获取时间线统计数据 — 使用 SQL 聚合代替 N+1 查询"""
    try:
        days = request.args.get('days', 30, type=int)
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)

        # 使用 SQL GROUP BY 聚合，一次查询获取全部结果
        photo_counts = dict(db.session.query(
            func.date(Photo.created_at),
            func.count(Photo.id)
        ).filter(
            Photo.created_at >= start_date,
            Photo.created_at <= end_date
        ).group_by(func.date(Photo.created_at)).all())

        video_counts = dict(db.session.query(
            func.date(Video.created_at),
            func.count(Video.id)
        ).filter(
            Video.created_at >= start_date,
            Video.created_at <= end_date
        ).group_by(func.date(Video.created_at)).all())

        diary_counts = dict(db.session.query(
            func.date(Diary.created_at),
            func.count(Diary.id)
        ).filter(
            Diary.created_at >= start_date,
            Diary.created_at <= end_date
        ).group_by(func.date(Diary.created_at)).all())

        # 生成日期列表并合并结果
        timeline_data = {}
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            date_obj = current_date.date()

            photos = photo_counts.get(date_obj, 0)
            videos = video_counts.get(date_obj, 0)
            diaries = diary_counts.get(date_obj, 0)

            timeline_data[date_str] = {
                'photos': photos,
                'videos': videos,
                'diaries': diaries,
                'total': photos + videos + diaries
            }
            current_date += timedelta(days=1)

        return jsonify({
            'timeline': timeline_data,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            }
        })

    except Exception as e:
        current_app.logger.error(f'获取时间线统计数据失败: {e}', exc_info=True)
        return jsonify({'error': '获取时间线统计数据失败'}), 500