from functools import wraps
from flask import request, jsonify
from flask_login import login_required, current_user

def admin_required(f):
    """需要管理员权限的装饰器"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # 确保是管理员
        if not current_user.is_authenticated or current_user.username != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        return f(*args, **kwargs)
    return decorated_function