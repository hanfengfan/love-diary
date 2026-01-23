import bcrypt

def generate_password_hash(password):
    """生成密码哈希"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, password_hash):
    """验证密码"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def allowed_file(filename, allowed_extensions):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions