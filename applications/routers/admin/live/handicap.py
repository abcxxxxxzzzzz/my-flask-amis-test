from flask import Blueprint, request,views,g
from applications.common.utils.validate import xss_escape
from applications.common.utils.http import Success,UpdateSuccess,DeleteSuccess,ParameterException,NotFound
from applications.common.helper import ModelFilter
from applications.models import Handicap
from applications.common.curd import model_to_dicts
from applications.schemas import HandicapOutSchema
from applications.extensions import db
from applications.common.utils.rights import authenticate
from applications.jsonp.live.json_handicap import getHandicapJson


admin_handicap = Blueprint('adminHandicap', __name__)

class HandicapTempAPIViews(views.MethodView):
    # decorators = [authenticate()]

    @authenticate(power='admin:handicap', log=False)
    def get(self):
        data = getHandicapJson(g.permissions)
        return Success(data=data)


class HandicapListAPIViews(views.MethodView):

    # decorators = [authenticate()]

    @authenticate(power='admin:handicap:list', log=False)
    def get(self):
        # 获取请求参数
        search = xss_escape(request.args.get('search', type=str))
        # 查询参数构造
        mf = ModelFilter()
        if search:
            mf.contains(field_name="name", value=search)

        # orm查询
        # 使用分页获取data需要.items
        obj = Handicap.query.filter(mf.get_filter(model=Handicap)).order_by(Handicap.create_at.desc()).layui_paginate()
        count = obj.total
        return Success(data={'rows': model_to_dicts(schema=HandicapOutSchema, data=obj.items), 'total': count})


class HandicapAPIViews(views.MethodView):
    def get(self, id):
        pass

    @authenticate(power='admin:handicap:add', log=True)
    def post(self):
        req_json = request.json
        name = xss_escape(req_json.get('name'))

        if not name:
            raise ParameterException(msg="此名称不能为空")

        if bool(Handicap.query.filter_by(name=name).count()):
            raise ParameterException(msg="此名称已经存在")

        obj = Handicap(name=name)
        db.session.add(obj)
        db.session.commit()
        return UpdateSuccess(msg="增加成功")

    @authenticate(power='admin:handicap:edit', log=True)
    def put(self, id):
        req_json = request.json
        name = xss_escape(req_json.get('name'))
        obj = Handicap.query.filter_by(id=id).update({'name': name})
        db.session.commit()
        if obj:
            return UpdateSuccess(msg="更新成功")
        return ParameterException(msg="更新失败")

    @authenticate(power='admin:handicap:del', log=True)
    def delete(self, id):
        obj = Handicap.query.filter_by(id=id).delete()
        db.session.commit()
        if not obj:
            return NotFound(msg="删除失败")
        return DeleteSuccess(msg="删除成功")





admin_handicap.add_url_rule('/handicap/temp',            view_func=HandicapTempAPIViews.as_view('handicapTemp'),         endpoint='handicapTemp',     methods=['GET'])        # 模板
admin_handicap.add_url_rule('/handicap/list',            view_func=HandicapListAPIViews.as_view('handicapList'),         endpoint='handicapList',     methods=['GET'])        # 列表
admin_handicap.add_url_rule('/handicap/<int:id>',        view_func=HandicapAPIViews.as_view('handicap'),                 endpoint='handicap',         methods=['GET','PUT','DELETE']) # 查改删
admin_handicap.add_url_rule('/handicap',                 view_func=HandicapAPIViews.as_view('handicapAdd'),              endpoint='handicapAdd',      methods=['POST'])                  # 增


