import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 检查必要的依赖
required_modules = ['flask', 'flask_sqlalchemy', 'flask_login', 'flask_cors']
missing_modules = []

for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    print("错误：缺少必要的依赖包，请先安装：")
    print(f"缺少的包: {', '.join(missing_modules)}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)

from app import create_app
from app.models import db, Admin

app = create_app()

if __name__ == '__main__':
    # 创建数据库
    with app.app_context():
        db.create_all()

        # 创建默认管理员账号
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            import secrets
            from app.utils.auth import generate_password_hash
            # 优先使用环境变量，否则随机生成安全密码（不使用固定弱密码）
            default_password = os.environ.get('ADMIN_PASSWORD') or secrets.token_urlsafe(16)
            default_admin = Admin(
                username='admin',
                password_hash=generate_password_hash(default_password)
            )
            db.session.add(default_admin)
            db.session.commit()
            logger.warning("=" * 50)
            logger.warning("默认管理员账号已创建: admin")
            if not os.environ.get('ADMIN_PASSWORD'):
                logger.warning(f"随机初始密码: {default_password}")
                logger.warning("请立即记录此密码，它不会再次显示！")
            logger.warning("请尽快登录后台修改密码，或通过 ADMIN_PASSWORD 环境变量预设密码")
            logger.warning("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)