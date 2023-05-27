
from flask import Blueprint, make_response, session, request, views,current_app, render_template
# from flask_login import  login_user, logout_user
from marshmallow import ValidationError

from applications.common import admin as index_curd
from applications.common.admin_log import login_log
from applications.common.utils.http import Success,NotFound,Forbidden,AuthFailed,ParameterException,DeleteSuccess
from applications.common.utils.rights import get_header_token,authenticate
from applications.common.utils.scherr import get_schema_errors
from applications.extensions import Redis
from applications.models import User
from applications.schemas import LoginSchema


auth_bp = Blueprint('adminAuth', __name__)

def register_auth_views(app):
    app.register_blueprint(auth_bp)



class AuthView(views.MethodView):

    def get(self):
        # return Success(msg='test')
        return render_template('login.html', title=current_app.config.get('SYSTEM_NAME'))


    def post(self):
        req = request.json
        try:
            load_req = LoginSchema().load(req)
        except ValidationError as err:
            return ParameterException(msg=get_schema_errors(err))

        username = load_req['username']
        password = load_req['password']

        if not username or not password:
            return ParameterException(msg="用户名或密码没有输入")

        user = User.query.filter_by(username=username).first()

        if user is None:
            return ParameterException(msg="不存在的用户")

        if user.enable == 0:
            return Forbidden(msg="用户被暂停使用")

        if username == user.username and user.validate_password(password):
            token = user.generate_auth_token(current_app.config['SECRET_KEY'], current_app.config['SECRET_EXPIRATION'])                  # 登录
            login_log(request, uid=user.id, is_access=True)     # 记录登录日志
            index_curd.add_auth_session(user)                       # 存入权限
            Redis.hset(name=current_app.config['REDIS_SAVE_TOKEN_NAME'], key=user.id, value=token)  # 存入数据库

            rsp = make_response(Success(msg="登录成功",data={'token': token})) # 设置请求头
            rsp.headers['X-Token'] = token
            return rsp

        # 记录日志
        login_log(request, uid=user.id, is_access=False)
        return AuthFailed(msg="用户名或密码错误")

    @authenticate()
    def delete(self):
        # logout_user()
        # session.pop('permissions')
        token = get_header_token()
        if token:
            user = User.verify_auth_token(token, current_app.config['SECRET_KEY'])
            if user:
                # 直接删除 Redis 当中的 Token，否则Token无效
                # pass
                Redis.hdel(name=current_app.config['REDIS_SAVE_TOKEN_NAME'], key=user.id)  # 存入数据库
                return DeleteSuccess(msg='已退出')
            else:
                return AuthFailed(msg='无效令牌')
        else:
            return NotFound(msg='未找到令牌')


auth_bp.add_url_rule('/login',  view_func=AuthView.as_view('login'),  methods=['GET','POST'],   endpoint='login')
auth_bp.add_url_rule('/logout', view_func=AuthView.as_view('logout'), methods=['DELETE'], endpoint='logout')



