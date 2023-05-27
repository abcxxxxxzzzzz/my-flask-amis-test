from flask import Blueprint, request,views,g
from applications.common.utils.validate import xss_escape
from applications.common.utils.http import Success,UpdateSuccess,DeleteSuccess,ParameterException,NotFound,Forbidden
from applications.common.helper import ModelFilter
from applications.models import User,Role,Handicap
from applications.common.curd import model_to_dicts, switch_status
from applications.schemas import UserOutSchema
from applications.extensions import db
from applications.common.utils.rights import authenticate
from applications.jsonp.rbac.jsonp_user import getUserJson


admin_user = Blueprint('adminUser', __name__)

class UserTempAPIViews(views.MethodView):
    # decorators = [authenticate()]

    @authenticate(power='admin:user', log=False)
    def get(self):
        data = getUserJson(g.permissions)
        return Success(data=data)


class UserListAPIViews(views.MethodView):

    # decorators = [authenticate()]

    @authenticate(power='admin:user:list', log=False)
    def get(self):
        # 获取请求参数
        search = xss_escape(request.args.get('search', type=str))
        # 查询参数构造
        mf = ModelFilter()
        if search:
            mf.contains(field_name="username", value=search)

        # orm查询
        # 使用分页获取data需要.items
        user = User.query.filter(mf.get_filter(model=User)).layui_paginate()
        count = user.total
        return Success(data={'rows': model_to_dicts(schema=UserOutSchema, data=user.items), 'total': count})


class UserAPIViews(views.MethodView):
    def get(self, id):
        pass

    @authenticate(power='admin:user:add', log=True)
    def post(self):
        req_json = request.json
        role_ids = req_json.get("roleIds",[])
        handicap_id = req_json.get("handicapId",None)
        username = xss_escape(req_json.get('username'))
        real_name = xss_escape(req_json.get('realname'))
        password = xss_escape(req_json.get('password'))
        enable = xss_escape(req_json.get('enable'))
        # role_ids = a.split(',')
        # print(username, real_name, password)

        if not username or not real_name or not password:
            raise ParameterException(msg="账号姓名密码不得为空")

        if bool(User.query.filter_by(username=username).count()):
            raise ParameterException(msg="用户已经存在")
        user = User(username=username, realname=real_name, enable=enable)
        user.set_password(password)
        db.session.add(user)
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        user.role = roles

        handicap = Handicap.query.get_or_404(handicap_id)
        user.handicap_id = handicap.id
        # for r in roles:
            # user.role.append(r)
        db.session.commit()
        return UpdateSuccess(msg="增加成功")

    @authenticate(power='admin:user:edit', log=True)
    def put(self, id):
        req_json = request.json
        role_ids = req_json.get("roleIds", [])
        handicap_id = req_json.get("handicapId", None)
        username = xss_escape(req_json.get('username'))
        realname = xss_escape(req_json.get('realname'))
        remark = xss_escape(req_json.get('remark'))
        # role_ids = a.split(',')
        User.query.filter_by(id=id).update({'username': username, 'realname': realname, 'remark': remark})
        u = User.query.filter_by(id=id).first()


        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        u.role = roles


        handicap = Handicap.query.filter(Handicap.id==handicap_id).first()
        if handicap:
            u.handicap_id = handicap.id
        else:
            u.handicap_id = None
        db.session.commit()
        return UpdateSuccess(msg="更新成功")

    @authenticate(power='admin:user:del', log=True)
    def delete(self, id):
        
        user = User.query.filter_by(id=id).first()
        if user.is_super:
            raise Forbidden(msg='不允许删除超级管理员')

        user.role = []
        
        res = User.query.filter_by(id=id)
        if not res:
            raise NotFound()

        res.delete()
        db.session.commit()
        return DeleteSuccess(msg="删除成功")


class UserSwitchAPIViews(views.MethodView):

    @authenticate("admin:user:edit", log=True)
    def put(self, id):
        req = request.json
        enable = xss_escape(req.get('enable'))
        # res = switch_status(model=User, id=id, enable=int(enable))
        res = User.query.get_or_404(id)
        if res.is_super:
            raise Forbidden(msg='不允许切换超级管理员')
        res.enable = int(enable)
        db.session.commit()

        if not res:
            return ParameterException(msg="出错啦")
        return Success(msg="状态已切换")


class UserPasswordAPIViews(views.MethodView):
    
    @authenticate(log=True)
    def put(self):
        res_json = request.json
        if res_json.get("newPassword") == '':
            return ParameterException("新密码不得为空")
        if res_json.get("newPassword") != res_json.get("repeatPassword"):
            return ParameterException("俩次密码不一样")
        user = g.user
        is_right = user.validate_password(res_json.get("oldPassword"))
        if not is_right:
            return ParameterException("旧密码错误")
        user.set_password(res_json.get("newPassword"))
        db.session.add(user)
        db.session.commit()
        return Success("更改成功")


class UserInfoAPIViews(views.MethodView):
    
    @authenticate(log=False)
    def get(self):
        return Success(data={"current_user": g.user.username })

admin_user.add_url_rule('/user/temp',            view_func=UserTempAPIViews.as_view('userTemp'),         endpoint='userTemp',     methods=['GET'])        # 模板
admin_user.add_url_rule('/user/list',            view_func=UserListAPIViews.as_view('userList'),         endpoint='userList',     methods=['GET'])        # 列表
admin_user.add_url_rule('/user/<int:id>',        view_func=UserAPIViews.as_view('user'),                 endpoint='user',         methods=['GET','PUT','DELETE']) # 查改删
admin_user.add_url_rule('/user',                 view_func=UserAPIViews.as_view('userAdd'),              endpoint='userAdd',      methods=['POST'])                  # 增
admin_user.add_url_rule('/user/status/<int:id>', view_func=UserSwitchAPIViews.as_view('userSwitch'),     endpoint='userSwitch',   methods=['PUT']) # 切换状态
admin_user.add_url_rule('/user/password',        view_func=UserPasswordAPIViews.as_view('userPassword'), endpoint='userPassword', methods=['PUT']) # 修改密码
admin_user.add_url_rule('/user/info',            view_func=UserInfoAPIViews.as_view('userInfo'),         endpoint='userInfo',     methods=['GET']) # 切换状态




# # 修改头像
# @admin_user.put('/updateAvatar')
# # @login_required
# def update_avatar():
#     url = request.json.get("avatar").get("src")
#     r = User.query.filter_by(id=current_user.id).update({"avatar": url})
#     db.session.commit()
#     if not r:
#         return fail_api(msg="出错啦")
#     return success_api(msg="修改成功")


# # 修改当前用户信息
# @admin_user.put('/updateInfo')
# # @login_required
# def update_info():
#     req_json = request.json
#     r = User.query.filter_by(id=current_user.id).update(
#         {"realname": req_json.get("realName"), "remark": req_json.get("details")})
#     db.session.commit()
#     if not r:
#         return fail_api(msg="出错啦")
#     return success_api(msg="更新成功")
