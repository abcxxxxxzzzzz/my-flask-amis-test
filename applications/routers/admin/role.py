from flask import Blueprint, request, views,g
from applications.common.utils.validate import xss_escape
from applications.common.utils.http import Success,UpdateSuccess,DeleteSuccess,ParameterException,NotFound,Forbidden
from applications.common.helper import ModelFilter
from applications.models import Role,Power
from applications.common.curd import model_to_dicts, switch_status
from applications.schemas import RoleOutSchema
from applications.extensions import db
from applications.common.utils.rights import authenticate
from applications.jsonp.rbac.jsonp_role import getRoleJson



admin_role = Blueprint('adminRole', __name__)


class RoleTempAPIViews(views.MethodView):
    # decorators = [authenticate()]

    @authenticate(power='admin:role', log=False)
    def get(self):
        data = getRoleJson(g.permissions)
        return Success(data=data)

class RoleListAPIViews(views.MethodView):

    # decorators = [authenticate()]

    @authenticate(power='admin:role:list', log=False)
    def get(self):
        # 获取请求参数
        search = xss_escape(request.args.get('search', type=str))
        # role_code = xss_escape(request.args.get('roleCode', type=str))
        # 查询参数构造
        mf = ModelFilter()
        if search:
            mf.vague(field_name="name", value=search)
        # orm查询
        # 使用分页获取data需要.items
        role = Role.query.filter(mf.get_filter(Role)).layui_paginate()
        count = role.total
        # 返回api
        return Success(data={'rows': model_to_dicts(schema=RoleOutSchema, data=role.items), 'total': count})

class RoleAPIViews(views.MethodView):

    @authenticate(power='admin:role:show', log=True)
    def get(self,id):
        pass

    @authenticate(power='admin:role:add', log=True)
    def post(self):
        req = request.json
        details = xss_escape(req.get("details"))
        enable = xss_escape(req.get("enable"))
        roleCode = xss_escape(req.get("roleCode"))
        roleName = xss_escape(req.get("roleName"))
        sort = xss_escape(req.get("sort"))
        role = Role(
            details=details,
            enable=enable,
            code=roleCode,
            name=roleName,
            sort=sort
        )
        db.session.add(role)
        db.session.commit()
        return Success(msg="成功")

    @authenticate(power='admin:role:edit', log=True)
    def put(self,id):
        req_json = request.json
        data = {
            "code": xss_escape(req_json.get("roleCode")),
            "name": xss_escape(req_json.get("roleName")),
            "sort": xss_escape(str(req_json.get("sort"))),
            "enable": xss_escape(req_json.get("enable")),
            "details": xss_escape(req_json.get("details"))
        }
        role = Role.query.filter_by(id=id)
        if role.first().code == 'role' and data['code'] != 'role' or int(data['enable']) != 1:
            raise Forbidden(msg='不允许修改或者禁用超级管理员角色标识')

        role.update(data)
        db.session.commit()
        if not role:
            raise NotFound(msg="更新角色失败")
        return UpdateSuccess(msg="更新角色成功")

    @authenticate(power='admin:role:del', log=True)
    def delete(self,id):
        role = Role.query.filter_by(id=id).first()
        if role.code == 'role':
            raise Forbidden(msg='不允许删除超级管理员角色')
        # 删除该角色的权限和用户
        role.power = []
        role.user = []
        
        r = Role.query.filter_by(id=id).delete()
        db.session.commit()
        if not r:
            return NotFound(msg="角色删除失败")
        return DeleteSuccess(msg="角色删除成功")

class RoleSwitchAPIViews(views.MethodView):
    
    @authenticate("admin:role:edit", log=True)
    def put(self, id):
        req = request.json
        enable = xss_escape(req.get('enable'))
        # res = switch_status(model=Role, id=id, enable=int(enable))

        res = Role.query.get_or_404(id)
        if res.code == 'role':
            raise Forbidden(msg='不允许切换超级管理员')
        res.enable = int(enable)
        db.session.commit()

        if not res:
            return ParameterException(msg="出错啦")
        return Success(msg="状态已切换")


admin_role.add_url_rule('/role/temp', view_func=RoleTempAPIViews.as_view('roleTemp'), endpoint='roleTemp', methods=['GET'])        # 模板
admin_role.add_url_rule('/role/list', view_func=RoleListAPIViews.as_view('roleList'), endpoint='roleList', methods=['GET'])        # 列表
admin_role.add_url_rule('/role/<int:id>', view_func=RoleAPIViews.as_view('role'), endpoint='role', methods=['GET','PUT','DELETE']) # 查改删
admin_role.add_url_rule('/role', view_func=RoleAPIViews.as_view('roleAdd'), endpoint='roleAdd', methods=['POST'])                  # 增
admin_role.add_url_rule('/role/status/<int:id>', view_func=RoleSwitchAPIViews.as_view('roleSwitch'), endpoint='roleSwitch', methods=['PUT']) # 切换状态

# 渲染权限
@admin_role.get('/role/power')
@authenticate("admin:role:edit", log=True)
def data2():
    from applications.schemas.admin_power import PowerOutSchema2
    from applications.common.admin import getTree
    obj = Power.query.all()
    rows = model_to_dicts(schema=PowerOutSchema2, data=obj)
    # print(rows)
    return Success(data={'options': getTree(rows)})




# 角色授权
@admin_role.post('/role/power/<int:id>')
@authenticate("admin:role:edit", log=True)
def save_role_power(id):
    req = request.json
    power_list = req.get("ids")
    role = Role.query.get_or_404(id)
    powers = Power.query.filter(Power.id.in_(power_list)).all()
    role.power = powers
    
    db.session.commit()
    return Success(msg="授权成功")



# #   用户分页查询
# @admin_role.get('/role')
# # @authorize("admin:user:main", log=True)
# def data():
#     # 获取请求参数
#     search = xss_escape(request.args.get('search', type=str))
#     # role_code = xss_escape(request.args.get('roleCode', type=str))
#     # 查询参数构造
#     mf = ModelFilter()
#     if search:
#         mf.vague(field_name="name", value=search)
#     # orm查询
#     # 使用分页获取data需要.items
#     role = Role.query.filter(mf.get_filter(Role)).layui_paginate()
#     count = role.total
#     # 返回api
#     return APIResponse.SUCCESS(data={'rows': model_to_dicts(schema=RoleOutSchema, data=role.items), 'total': count})



# 角色增加
# @admin_role.post('/role')
# # @authorize("admin:role:add", log=True)
# def save():
#     req = request.json
#     details = xss_escape(req.get("details"))
#     enable = xss_escape(req.get("enable"))
#     roleCode = xss_escape(req.get("roleCode"))
#     roleName = xss_escape(req.get("roleName"))
#     sort = xss_escape(req.get("sort"))
#     role = Role(
#         details=details,
#         enable=enable,
#         code=roleCode,
#         name=roleName,
#         sort=sort
#     )
#     db.session.add(role)
#     db.session.commit()
#     return APIResponse.SUCCESS(msg="成功")



# # 角色删除
# @admin_role.delete('/role/<int:id>')
# # @authorize("admin:role:remove", log=True)
# def remove(id):
#     role = Role.query.filter_by(id=id).first()
#     # 删除该角色的权限和用户
#     role.power = []
#     role.user = []
    
#     r = Role.query.filter_by(id=id).delete()
#     db.session.commit()
#     if not r:
#         return APIResponse.FAILED(msg="角色删除失败")
#     return APIResponse.SUCCESS(msg="角色删除成功")



# # 更新角色
# @admin_role.put('/role/<int:id>')
# # @authorize("admin:role:edit", log=True)
# def update(id):
#     req_json = request.json
#     data = {
#         "code": xss_escape(req_json.get("roleCode")),
#         "name": xss_escape(req_json.get("roleName")),
#         "sort": xss_escape(str(req_json.get("sort"))),
#         "enable": xss_escape(req_json.get("enable")),
#         "details": xss_escape(req_json.get("details"))
#     }
#     role = Role.query.filter_by(id=id).update(data)
#     db.session.commit()
#     if not role:
#         return APIResponse.FAILED(msg="更新角色失败")
#     return APIResponse.SUCCESS(msg="更新角色成功")









