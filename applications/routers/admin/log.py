from flask import Blueprint, render_template, request, current_app, views,g
from applications.common.utils.validate import xss_escape
from applications.common.utils.http import Success,UpdateSuccess,DeleteSuccess,ParameterException,NotFound
from applications.common.helper import ModelFilter
from applications.models import AdminLog
from applications.common.curd import model_to_dicts, switch_status
from applications.schemas import LogOutSchema
from applications.extensions import db
from applications.common.utils.rights import authenticate
from applications.jsonp.rbac.jsonp_log import getLogJson



admin_log = Blueprint('adminLog', __name__)


class logTempAPIViews(views.MethodView):

    @authenticate(power='admin:log', log=False)
    def get(self):
        data = getLogJson(g.permissions)
        return Success(data=data)


class LogListAPIViews(views.MethodView):

    @authenticate(power='admin:log:list', log=False)
    def get(self):
        # 获取请求参数
        search = xss_escape(request.args.get('search', type=str))
        # role_code = xss_escape(request.args.get('roleCode', type=str))
        # 查询参数构造
        mf = ModelFilter()
        if search:
            mf.vague(field_name="ip", value=search)
        # orm查询
        # 使用分页获取data需要.items
        obj = AdminLog.query.filter(mf.get_filter(AdminLog)).order_by(AdminLog.create_time.desc()).layui_paginate()
        count = obj.total
        # 返回api
        return Success(data={'rows': model_to_dicts(schema=LogOutSchema, data=obj.items), 'total': count})

    @authenticate(power="admin:log:batch:del", log=True)
    def delete(self,ids):
        _ids = ids.split(',') or list(ids)
        obj = AdminLog.query.filter(AdminLog.id.in_(_ids)).delete(synchronize_session=False)
        db.session.commit()
        if obj:
            return Success(msg="删除成功")
        else:
            return ParameterException(msg="删除失败")


admin_log.add_url_rule('/log/temp', view_func=logTempAPIViews.as_view('logemp'), endpoint='logTemp', methods=['GET'])                    # 模板
admin_log.add_url_rule('/log/list', view_func=LogListAPIViews.as_view('logList'), endpoint='logList', methods=['GET'])                   # 列表
admin_log.add_url_rule('/log/batch/<ids>', view_func=LogListAPIViews.as_view('logBatchDel'), endpoint='logBatchDel', methods=['DELETE'])        # 批量删除