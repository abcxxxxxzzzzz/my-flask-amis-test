from flask import  make_response, render_template, Blueprint, g,request,current_app
from applications.common.utils.http import Success, AuthFailed
from applications.common.utils.rights import authenticate
from applications.common.admin import make_menu_tree
from applications.models.admin_rbac import User

index_bp = Blueprint('adminIndex', __name__)


# 不能定义权限验证控件
@index_bp.route('/temp/index')
# @authenticate()
def get_index():
    # print(request.headers.get(current_app.config['HEADER_TOKEN_NAME']))
    # token = request.args.get('X-Token', None)
    # if token is None:
    #     return AuthFailed(msg='无效令牌')
    # verify = User.verify_auth_token(token, current_app.config['SECRET_KEY'])
    # if not verify:
    #     return AuthFailed(msg='无效令牌')
    # print(request.headers.get(current_app.config['HEADER_TOKEN_NAME']))
    return render_template('index.html', title=current_app.config.get('SYSTEM_NAME'))


# 渲染菜单
@index_bp.route('/temp/menu')
@authenticate()
def get_menu():
    data = make_menu_tree()
    return Success(data=data)
    from applications.jsonp.menu.admin_menu import menu
    return Success(data=menu)


# # 渲染菜单
# @index_bp.route('/temp/user')
# def get_user():
#     from applications.jsonp.rbac.jsonp_user import userJson
#     return APIResponse.SUCCESS(data=userJson)


# # 渲染角色
# @index_bp.route('/temp/role')
# def get_role():
#     from applications.jsonp.rbac.jsonp_role import roleJson
#     return APIResponse.SUCCESS(data=roleJson)



# # 渲染权限
# @index_bp.route('/temp/power')
# def get_power():
#     from applications.jsonp.rbac.jsonp_power import powerJson
#     return APIResponse.SUCCESS(data=powerJson)
