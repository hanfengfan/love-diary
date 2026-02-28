from datetime import datetime, timezone
from .database import db


def _utcnow():
    return datetime.now(timezone.utc)


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False, default=1)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    thumbnail = db.Column(db.String(500))
    category = db.Column(db.String(100), default='日常')
    tags = db.Column(db.String(500), default='')
    duration = db.Column(db.Integer)  # 秒数
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def __repr__(self):
        return f'<Video {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'filename': self.filename,
            'filepath': self.filepath,
            'thumbnail': self.thumbnail,
            'category': self.category,
            'tags': self.tags.split(',') if self.tags else [],
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }