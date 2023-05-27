from flask import Blueprint, request,views,g
from applications.common.utils.validate import xss_escape
from applications.common.utils.http import Success,UpdateSuccess,DeleteSuccess,ParameterException,NotFound,Forbidden
from applications.common.helper import ModelFilter
from applications.models import HTTPSDomain
from applications.common.curd import model_to_dicts,switch_status
from applications.schemas import HTTPSDomainOutSchema
from applications.extensions import db
from applications.common.utils.rights import authenticate
from applications.jsonp.other.json_domain_https import getJson
from sqlalchemy import or_,and_
from sqlalchemy import text


admin_domain_https = Blueprint('adminDomainHTTPS', __name__)

class HTTPSTempAPIViews(views.MethodView):
    # decorators = [authenticate()]

    @authenticate(power='admin:domain:https', log=False)
    def get(self):
        data = getJson(g.permissions)
        return Success(data=data)


class HTTPSListAPIViews(views.MethodView):

    # decorators = [authenticate()]

    @authenticate(power='admin:domain:https:list', log=False)
    def get(self):
        # 获取请求参数
        search = xss_escape(request.args.get('search', type=str))
        orderBy = xss_escape(request.args.get('orderBy', type=str))
        orderDir = xss_escape(request.args.get('orderDir', type=str))
        # 查询参数构造
        mf = ModelFilter()
        if search:
            mf.contains(field_name="name", value=search)

        # orm查询
        # 使用分页获取data需要.items

        if orderBy and orderDir == 'desc':
            obj = HTTPSDomain.query.filter(mf.get_filter(model=HTTPSDomain)).order_by(HTTPSDomain.expir_day.desc()).layui_paginate()
        elif orderBy and orderDir == 'asc':
            obj = HTTPSDomain.query.filter(mf.get_filter(model=HTTPSDomain)).order_by(HTTPSDomain.expir_day.asc()).layui_paginate()
        else:
            obj = HTTPSDomain.query.filter(mf.get_filter(model=HTTPSDomain)).order_by(HTTPSDomain.create_at.desc()).layui_paginate()


        # obj = Tag.query.filter(mf.get_filter(model=Tag)).order_by(Tag.create_at.desc()).layui_paginate()
        count = obj.total
        return Success(data={'rows': model_to_dicts(schema=HTTPSDomainOutSchema, data=obj.items), 'total': count})

    @authenticate(power='admin:domain:https:batch:add', log=True)
    def post(self):
        req = request.json
        handicap_id = req['handicapId']
        batchAdd = req['batchadd']
        if batchAdd:
            _many = batchAdd.split('\n') or list[batchAdd]
            db_data = [ {"name": m.replace(" ",''), 'enable': 1, 'handicap_id': handicap_id } for m in _many ]
            try:
                db.session.execute(
                    HTTPSDomain.__table__.insert(),
                    db_data
                )
                db.session.commit()
                return Success(msg='批量添加成功')
            except Exception as e:
                raise ParameterException(msg='批量添加失败: 错误详情: {0}'.format(str(e)))
        return ParameterException(msg='请输入需要添加的数据')

    @authenticate(power='admin:domain:https:batch:del', log=True)
    def delete(self):
        req = request.json
        ids = req['ids']
        _ids = ids.split(',') or list(ids)
        title = HTTPSDomain.query.filter(HTTPSDomain.id.in_(_ids)).delete(synchronize_session=False)
        db.session.commit()
        if title:
            return Success(msg="删除成功")
        else:
            return ParameterException(msg="删除失败")


class HTTPSAPIViews(views.MethodView):
    def get(self, id):
        pass

    @authenticate(power='admin:domain:https:add', log=True)
    def post(self):
        req_json = request.json
        name = req_json.get('name')
        remark = req_json.get('remark')
        handicap_id = req_json.get('handicapId')

        if not name or not handicap_id:
            raise ParameterException(msg="域名或部门不能为空")


        is_exist = HTTPSDomain.query.filter(HTTPSDomain.name==name).first()
        if is_exist:
            raise ParameterException(msg="此域名已经存在")

        obj = HTTPSDomain(name=name,handicap_id=handicap_id, enable=1,remark=remark or '')
        db.session.add(obj)
        db.session.commit()
        if not obj:
            raise ParameterException(msg='添加失败')
        return UpdateSuccess(msg="增加成功")

    @authenticate(power='admin:domain:https:edit', log=True)
    def put(self, id):
        req_json = request.json
        name = xss_escape(req_json.get('name'))
        remark = xss_escape(req_json.get('remark'))

        obj = HTTPSDomain.query.filter_by(name=name).first()
        if obj and obj.id != int(id):
            raise ParameterException(msg='域名已存在')

        obj = HTTPSDomain.query.filter_by(id=id).update({'remark': remark, 'name': name})
        db.session.commit()
        if obj:
            return UpdateSuccess(msg="更新成功")
        return ParameterException(msg="更新失败")

    @authenticate(power='admin:domain:https:del', log=True)
    def delete(self, id):
        obj = HTTPSDomain.query.filter_by(id=id)
        obj.delete()
        db.session.commit()
        if not obj:
            return NotFound(msg="删除失败")
        return DeleteSuccess(msg="删除成功")



class HTTPSSwitchAPIViews(views.MethodView):

    @authenticate("admin:domain:https:edit", log=True)
    def put(self, id):
        req = request.json
        enable = xss_escape(req.get('enable'))
        res = switch_status(model=HTTPSDomain, id=id, enable=int(enable))
        # res.enable = int(enable)
        # db.session.commit()

        if not res:
            return ParameterException(msg="出错啦")
        return Success(msg="状态已切换")



admin_domain_https.add_url_rule('/domain/https/temp',            view_func=HTTPSTempAPIViews.as_view('httpsTemp'),         endpoint='httpsTemp',     methods=['GET'])        # 模板
admin_domain_https.add_url_rule('/domain/https/list',            view_func=HTTPSListAPIViews.as_view('httpsList'),         endpoint='httpsList',     methods=['GET'])        # 列表
admin_domain_https.add_url_rule('/domain/https/batch',           view_func=HTTPSListAPIViews.as_view('httpsBatchAdd'),     endpoint='httpsBatchAdd',methods=['POST','DELETE'])        # 列表
admin_domain_https.add_url_rule('/domain/https/<int:id>',        view_func=HTTPSAPIViews.as_view('https'),                 endpoint='https',         methods=['GET','PUT','DELETE']) # 查改删
admin_domain_https.add_url_rule('/domain/https',                 view_func=HTTPSAPIViews.as_view('httpsAdd'),              endpoint='httpsAdd',      methods=['POST'])                  # 增
admin_domain_https.add_url_rule('/domain/https/status/<int:id>', view_func=HTTPSSwitchAPIViews.as_view('httpsSwitch'),  endpoint='httpsSwitch',      methods=['PUT'])                  # 增


