from functools import wraps
from flask import abort
from flask_login import current_user

# 定义两个装饰器

# 检测普通权限
def permission_required(permission):
    def decorator(f):
        @wraps(f)  # 此处作用: decorated_function.__name__ = f.__name__, 这样，原函数的函数名经过装饰后将不会改变
        def decorated_function(*args, **kwargs): # 参数 *为一个元祖 **为一个字典, 任意参数都能配置
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 检测管理员权限
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)