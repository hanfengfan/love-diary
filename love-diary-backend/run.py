import os
import sys

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
            from app.utils.auth import generate_password_hash
            default_admin = Admin(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(default_admin)
            db.session.commit()
            print("默认管理员账号创建成功: admin / admin123")

    app.run(debug=True, host='0.0.0.0', port=5000)