from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from .models.database import db
import os
import secrets
import logging

login_manager = LoginManager()
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    # 配置
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
    app.config['ALLOWED_PHOTO_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['ALLOWED_VIDEO_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'wmv'}

    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'photos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails'), exist_ok=True)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'],
         supports_credentials=True)

    # 登录管理器配置
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Admin
        return Admin.query.get(int(user_id))

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.photos import photos_bp
    from app.routes.videos import videos_bp
    from app.routes.diaries import diaries_bp
    from app.routes.search import search_bp
    from app.routes.timeline import timeline_bp
    from app.routes.statistics import statistics_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(photos_bp, url_prefix='/api/photos')
    app.register_blueprint(videos_bp, url_prefix='/api/videos')
    app.register_blueprint(diaries_bp, url_prefix='/api/diaries')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(timeline_bp, url_prefix='/api/timeline')
    app.register_blueprint(statistics_bp, url_prefix='/api/statistics')

    # 静态文件服务
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        from flask import send_from_directory
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app