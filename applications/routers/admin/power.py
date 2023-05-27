from flask import Blueprint, request, views,g
from applications.common.utils.validate import xss_escape
from applications.common.utils.http import Success,UpdateSuccess,DeleteSuccess,ParameterException,NotFound
from applications.common.helper import ModelFilter
from applications.models import Power
from applications.common.curd import model_to_dicts, switch_status
from applications.schemas import PowerOutSchema
from applications.extensions import db
from applications.common.utils.rights import authenticate
from applications.common.admin import getTree
from applications.jsonp.rbac.jsonp_power import getPowerJson



admin_power = Blueprint('adminPower', __name__)


class PowerTempAPIViews(views.MethodView):

    # decorators = [authenticate()]

    @authenticate(power='admin:power', log=False)
    def get(self):
        data = getPowerJson(g.permissions)
        return Success(data=data)

class PowerListAPIViews(views.MethodView):

    # decorators = [authenticate()]

    @authenticate(power='admin:power:list', log=False)
    def get(self):
        # 获取请求参数
        search = xss_escape(request.args.get('search', type=str))
        # 查询参数构造
        mf = ModelFilter()
        if search:
            mf.contains(field_name="name", value=search)

        # mf.exact(field_name="type", value=0)
        # orm查询
        # 使用分页获取data需要.items
        # obj = Power.query.filter(mf.get_filter(model=Power)).layui_paginate()
        obj = Power.query.filter(mf.get_filter(model=Power)).layui_paginate()
        count = obj.total
        # 返回api data={'rows': json_data, 'total': total}
        # return APIResponse.SUCCESS(data=model_to_dicts(schema=UserOutSchema, data=user.items), count=count)

        # from applications.common.admin import make_menu_tree
        # print(make_menu_tree())
        rows = model_to_dicts(schema=PowerOutSchema, data=obj.items)
        new_rows = getTree(rows)
        return Success(data={'rows': new_rows, 'total': count})

class PowerAPIViews(views.MethodView):

    @authenticate(power='admin:power:list', log=True)
    def get(self, id=None):
        if not id:
            from applications.schemas.admin_power import PowerOutSchema2
            from applications.common.admin import getTree
            obj = Power.query.all()
            rows = model_to_dicts(schema=PowerOutSchema2, data=obj)
            # print(rows)
            return Success(data={'options': getTree(rows)})
        pass

    @authenticate(power='admin:power:add', log=True)
    def post(self):
        req = request.json
        parentId = int(req.get("parent_id", 0))
        icon = xss_escape(req.get("icon"))
        openType = xss_escape(req.get("open_type"))
        powerCode = xss_escape(req.get("code"))
        powerName = xss_escape(req.get("name"))
        powerType = xss_escape(req.get("type"))
        powerUrl = xss_escape(req.get("url"))
        # schemaUrl = xss_escape(req.get("schema_url"))
        sort = xss_escape(req.get("sort"))
        power = Power(
            icon=icon,
            open_type=openType,
            parent_id=parentId,
            code=powerCode,
            name=powerName,
            type=powerType,
            url=powerUrl,
            # schema_url=schemaUrl,
            sort=sort,
            enable=1
        )
        db.session.add(power)
        db.session.commit()
        return UpdateSuccess(msg="成功")

    @authenticate(power='admin:power:edit', log=True)
    def put(self, id):
        req_json = request.json
        data = {
            "icon": xss_escape(req_json.get("icon")),
            "open_type": xss_escape(req_json.get("open_type")),
            "parent_id": int(req_json.get("parent_id",0)),
            "code": xss_escape(req_json.get("code")),
            "name": xss_escape(req_json.get("name")),
            "type": xss_escape(req_json.get("type")),
            "url": xss_escape(req_json.get("url")),
            # "schema_url": xss_escape(req_json.get("schema_url")),
            "sort": xss_escape(str(req_json.get("sort")))
        }
        res = Power.query.filter_by(id=id).update(data)
        db.session.commit()
        if not res:
            raise NotFound(msg="更新权限失败")
        return UpdateSuccess(msg="更新权限成功")

    @authenticate(power='admin:power:del', log=True)
    def delete(self, id):
        power = Power.query.filter_by(id=id).first()
        power.role = []

        r = Power.query.filter_by(id=id).delete()
        db.session.commit()
        if not r:
            return NotFound(msg="删除失败")
        return Success(msg="删除成功")
            
class PowerSwitchAPIViews(views.MethodView):
    
    @authenticate("admin:power:edit", log=True)
    def put(self, id):
        req = request.json
        enable = xss_escape(req.get('enable'))
        res = switch_status(model=Power, id=id, enable=int(enable))
        if not res:
            return ParameterException(msg="出错啦")
        return Success(msg="状态已切换")

admin_power.add_url_rule('/power/temp', view_func=PowerTempAPIViews.as_view('powerTemp'), endpoint='powerTemp', methods=['GET'])        # 模板
admin_power.add_url_rule('/power/list', view_func=PowerListAPIViews.as_view('powerList'), endpoint='powerList', methods=['GET'])        # 列表
admin_power.add_url_rule('/power/<int:id>', view_func=PowerAPIViews.as_view('power'), endpoint='power', methods=['GET','PUT','DELETE']) # 查改删
admin_power.add_url_rule('/power', view_func=PowerAPIViews.as_view('addpower'), endpoint='addpower', methods=['GET','POST'])            # 增，渲染角色编辑权限内容
admin_power.add_url_rule('/power/status/<int:id>', view_func=PowerSwitchAPIViews.as_view('powerSwitch'), endpoint='powerSwitch', methods=['PUT']) # 切换状态



# #  权限分页查询
# @admin_power.get('/power')
# # @authorize("admin:user:main", log=True)
# # @authenticate()
# def data():
#     # 获取请求参数
#     search = xss_escape(request.args.get('search', type=str))
#     # 查询参数构造
#     mf = ModelFilter()
#     if search:
#         mf.contains(field_name="username", value=search)

#     # orm查询
#     # 使用分页获取data需要.items
#     obj = Power.query.filter(mf.get_filter(model=Power)).layui_paginate()
#     # count = obj.total
#     # 返回api data={'rows': json_data, 'total': total}
#     # return APIResponse.SUCCESS(data=model_to_dicts(schema=UserOutSchema, data=user.items), count=count)

#     # from applications.common.admin import make_menu_tree
#     # print(make_menu_tree())
#     rows = model_to_dicts(schema=PowerOutSchema, data=obj.items)
#     new_rows = getTree(rows)
#     return APIResponse.SUCCESS(data={'rows': new_rows, 'total': len(new_rows)})




# # 增加
# @admin_power.post('/power')
# # @authorize("admin:power:add", log=True)
# def save():
#     req = request.json
#     icon = xss_escape(req.get("icon"))
#     openType = xss_escape(req.get("open_type"))
#     parentId = xss_escape(req.get("parent_id"))
#     powerCode = xss_escape(req.get("code"))
#     powerName = xss_escape(req.get("name"))
#     powerType = xss_escape(req.get("type"))
#     powerUrl = xss_escape(req.get("url"))
#     # schemaUrl = xss_escape(req.get("schema_url"))
#     sort = xss_escape(req.get("sort"))
#     power = Power(
#         icon=icon,
#         open_type=openType,
#         parent_id=parentId,
#         code=powerCode,
#         name=powerName,
#         type=powerType,
#         url=powerUrl,
#         # schema_url=schemaUrl,
#         sort=sort,
#         enable=1
#     )
#     db.session.add(power)
#     db.session.commit()
#     return APIResponse.SUCCESS(msg="成功")



# # 权限删除
# @admin_power.delete('/power/<int:id>')
# # @authorize("admin:power:remove", log=True)
# def remove(id):
#     power = Power.query.filter_by(id=id).first()
#     power.role = []

#     r = Power.query.filter_by(id=id).delete()
#     db.session.commit()
#     if r:
#         return APIResponse.SUCCESS(msg="删除成功")
#     else:
#         return APIResponse.FAILED(msg="删除失败")


# # 权限更新
# @admin_power.put('/power/<int:id>')
# # @authorize("admin:power:edit", log=True)
# def update(id):
#     req_json = request.json
#     data = {
#         "icon": xss_escape(req_json.get("icon")),
#         "open_type": xss_escape(req_json.get("open_type")),
#         "parent_id": xss_escape(str(req_json.get("parent_id"))),
#         "code": xss_escape(req_json.get("code")),
#         "name": xss_escape(req_json.get("name")),
#         "type": xss_escape(req_json.get("type")),
#         "url": xss_escape(req_json.get("url")),
#         # "schema_url": xss_escape(req_json.get("schema_url")),
#         "sort": xss_escape(str(req_json.get("sort")))
#     }
#     res = Power.query.filter_by(id=id).update(data)
#     db.session.commit()
#     if not res:
#         return APIResponse.FAILED(msg="更新权限失败")
#     return APIResponse.SUCCESS(msg="更新权限成功")
