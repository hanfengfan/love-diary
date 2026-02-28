from flask import Blueprint, request, jsonify, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Admin, db
from app.utils.auth import check_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """管理员登录"""
    try:
        data = request.get_json()

        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': '用户名和密码不能为空'}), 400

        username = data.get('username')
        password = data.get('password')

        # 查找管理员
        admin = Admin.query.filter_by(username=username).first()

        if not admin or not check_password(password, admin.password_hash):
            return jsonify({'error': '用户名或密码错误'}), 401

        # 登录
        login_user(admin, remember=True)

        return jsonify({
            'message': '登录成功',
            'user': {
                'id': admin.id,
                'username': admin.username
            }
        })

    except Exception as e:
        current_app.logger.error(f'登录失败: {e}', exc_info=True)
        return jsonify({'error': '登录失败，请稍后重试'}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """管理员登出"""
    try:
        logout_user()
        return jsonify({'message': '登出成功'})
    except Exception as e:
        current_app.logger.error(f'登出失败: {e}', exc_info=True)
        return jsonify({'error': '登出失败'}), 500

@auth_bp.route('/check', methods=['GET'])
def check_login():
    """检查登录状态"""
    if current_user.is_authenticated:
        return jsonify({
            'logged_in': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username
            }
        })
    else:
        return jsonify({
            'logged_in': False
        })

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """修改管理员密码"""
    try:
        data = request.get_json()

        if not data or not data.get('old_password') or not data.get('new_password'):
            return jsonify({'error': '旧密码和新密码不能为空'}), 400

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        # 验证旧密码
        if not check_password(old_password, current_user.password_hash):
            return jsonify({'error': '旧密码错误'}), 401

        # 检查新密码长度
        if len(new_password) < 6:
            return jsonify({'error': '新密码长度不能少于6位'}), 400

        # 更新密码
        from app.utils.auth import generate_password_hash
        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({'message': '密码修改成功'})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'密码修改失败: {e}', exc_info=True)
        return jsonify({'error': '密码修改失败'}), 500