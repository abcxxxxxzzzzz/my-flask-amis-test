from functools import wraps
from flask import abort, request, jsonify, session
from flask_login import login_required
from applications.common.admin_log import admin_log
from applications.common.admin import add_auth_session

# def authorize(power: str, log: bool = False):
#     def decorator(func):
#         @login_required
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             if not power in session.get('permissions'):
#                 if log:
#                     admin_log(request=request, is_access=False)
#                 if request.method == 'GET':
#                     abort(403)
#                 else:
#                     return jsonify(success=False, msg="权限不足!")
#             if log:
#                 admin_log(request=request, is_access=True)
#             return func(*args, **kwargs)

#         return wrapper

#     return decorator







from functools import wraps
from flask import request,g,current_app
from applications.models import User
from applications.common.utils.http import AuthFailed,Forbidden

# 自定义全局认证装饰器
def authenticate(power: str = None, log: bool = False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            auth = verify_token()                                     # 判断是否已登录，并重新赋值权限
            if auth: 
                if power is not None and  power not in g.permissions: # 判断是否有权限参数，如果没有就直接过去
                    if log:                                           # 判断是否启用日志，记录日志
                        admin_log(request=request, is_access=False)   
                    raise Forbidden()

                if log:
                        admin_log(request=request, is_access=True)
                return fn(*args, **kwargs)

            else:
                raise AuthFailed()
                # return APIResponse.FAILED(msg="无效Token")
        return decorator
    return wrapper

# 获取 Token
def get_header_token():
    # print(request.args)
    token = request.headers.get(current_app.config['HEADER_TOKEN_NAME'])
    # print(token)

    # if request.path == "/admin/temp/index" and token is None:
    #     token = request.args.get(current_app.config['HEADER_TOKEN_NAME'],None)
    
    if token is None:
        raise AuthFailed('无效令牌')
    return token


# 一种基于 Token
# @auth.verify_password                              # 定义校验密码的回调函数
def verify_token():
    """从头部获取 token """
    token = get_header_token()
    # 先验证 Token 是否有效，如果Token无效或者没有Token,则验证用户密码
    user = User.verify_auth_token(token, current_app.config['SECRET_KEY'])
    if not user:
        return False
    g.permissions = add_auth_session(user)          # 存储用户的权限
    # print(g.permissions)
    g.user = user                                   # 存储用户
    return True                                     # 校验通过返回True