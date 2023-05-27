from flask import Blueprint, request,views,g
from applications.common.utils.validate import xss_escape
from applications.common.utils.http import Success,UpdateSuccess,DeleteSuccess,ParameterException,NotFound,Forbidden
from applications.common.helper import ModelFilter
from applications.models import Tag
from applications.common.curd import model_to_dicts
from applications.schemas import TagOutSchema
from applications.extensions import db
from applications.common.utils.rights import authenticate
from applications.jsonp.live.json_tag import getJson
from sqlalchemy import or_,and_


admin_tag = Blueprint('adminTag', __name__)

class TagTempAPIViews(views.MethodView):
    # decorators = [authenticate()]

    @authenticate(power='admin:tag', log=False)
    def get(self):
        data = getJson(g.permissions)
        return Success(data=data)


class TagListAPIViews(views.MethodView):

    # decorators = [authenticate()]

    @authenticate(power='admin:tag:list', log=False)
    def get(self):
        # 获取请求参数
        search = xss_escape(request.args.get('search', type=str))

        # 查询参数构造
        mf = ModelFilter()
        if search:
            mf.contains(field_name="name", value=search)

        # orm查询
        # 使用分页获取data需要.items

        if g.user.is_super:
            obj = Tag.query.filter(mf.get_filter(model=Tag)).order_by(Tag.create_at.desc()).layui_paginate()
        else:
            obj = Tag.query.filter(Tag.handicap_id==g.user.handicap_id).filter(mf.get_filter(model=Tag)).order_by(Tag.create_at.desc()).layui_paginate()


        # obj = Tag.query.filter(mf.get_filter(model=Tag)).order_by(Tag.create_at.desc()).layui_paginate()
        count = obj.total
        return Success(data={'rows': model_to_dicts(schema=TagOutSchema, data=obj.items), 'total': count})


class TagAPIViews(views.MethodView):
    def get(self, id):
        pass

    @authenticate(power='admin:tag:add', log=True)
    def post(self):
        req_json = request.json
        name = xss_escape(req_json.get('name'))
        color = xss_escape(req_json.get('color'))


        handicap_id = None
        if g.user.is_super:
            handicap_id = req_json.get('handicapId', None)
        else:
            handicap_id = g.user.handicap_id


        if not name:
            raise ParameterException(msg="此名称不能为空")

        is_exist = Tag.query.filter(and_(Tag.name==name, Tag.handicap_id==handicap_id)).first()
        if is_exist:
            raise ParameterException(msg="此名称已经存在")

        obj = Tag(name=name, color=color, handicap_id=handicap_id)
        db.session.add(obj)
        db.session.commit()
        if not obj:
            raise ParameterException(msg='添加失败')
        return UpdateSuccess(msg="增加成功")

    @authenticate(power='admin:tag:edit', log=True)
    def put(self, id):
        req_json = request.json
        name = xss_escape(req_json.get('name'))
        color = xss_escape(req_json.get('color'))

        handicap_id = None
        if g.user.is_super:
            handicap_id = req_json.get('handicapId', None)
        else:
            handicap_id = g.user.handicap_id

        is_exist = Tag.query.filter(and_(Tag.name==name, Tag.handicap_id==handicap_id)).first()
        if is_exist and is_exist.id == handicap_id:
            raise ParameterException(msg="此名称已经存在")


        obj = Tag.query.filter_by(id=id).update({'name': name, 'color': color, 'handicap_id': handicap_id})
        db.session.commit()
        if obj:
            return UpdateSuccess(msg="更新成功")
        return ParameterException(msg="更新失败")

    @authenticate(power='admin:tag:del', log=True)
    def delete(self, id):
        obj = Tag.query.filter_by(id=id)
        if not g.user.is_super and obj.first().handicap_id != g.user.handicap_id:
            raise Forbidden()
            
        obj.delete()
        db.session.commit()
        if not obj:
            return NotFound(msg="删除失败")
        return DeleteSuccess(msg="删除成功")





admin_tag.add_url_rule('/tag/temp',            view_func=TagTempAPIViews.as_view('tagTemp'),         endpoint='tagTemp',     methods=['GET'])        # 模板
admin_tag.add_url_rule('/tag/list',            view_func=TagListAPIViews.as_view('tagList'),         endpoint='tagList',     methods=['GET'])        # 列表
admin_tag.add_url_rule('/tag/<int:id>',        view_func=TagAPIViews.as_view('tag'),                 endpoint='tag',         methods=['GET','PUT','DELETE']) # 查改删
admin_tag.add_url_rule('/tag',                 view_func=TagAPIViews.as_view('tagAdd'),              endpoint='tagAdd',      methods=['POST'])                  # 增


