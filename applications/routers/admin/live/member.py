from flask import Blueprint, request,views,g
from applications.common.utils.validate import xss_escape
from applications.common.utils.http import Success,UpdateSuccess,DeleteSuccess,ParameterException,NotFound,ServerError,Forbidden
from applications.common.helper import ModelFilter
from applications.models import Member,Handicap,Tag
from applications.common.curd import model_to_dicts
from applications.schemas import MemberOutSchema, HandicapOutSchema
from applications.extensions import db
from applications.common.utils.rights import authenticate
from applications.jsonp.live.jsonp_member import getMemberJson
from sqlalchemy import or_,and_
from sqlalchemy.orm import Session
import datetime


admin_member = Blueprint('adminMember', __name__)

class MemberTempAPIViews(views.MethodView):
    # decorators = [authenticate()]

    @authenticate(power='admin:member', log=False)
    def get(self):
        data = getMemberJson(g.permissions)
        return Success(data=data)


class MemberListAPIViews(views.MethodView):

    # decorators = [authenticate()]

    @authenticate(power='admin:member:list', log=False)
    def get(self):
        # 盘口ID多选： 1,2,3
        ids = xss_escape(request.args.get('ids', type=str))

        # 标签ID多选： 1,2,3
        tags = xss_escape(request.args.get('tags', type=str))

        # 获取请求参数
        search = xss_escape(request.args.get('search', type=str))
        more = xss_escape(request.args.get('more', type=str))


        # -----------------------------  多条件查询开始 ----------------------------
        filters = []

        
        # 多查
        if more:
            filters.append(or_(
            Member.username.like('%' + more + '%'),
            Member.realname.like('%' + more + '%'),
            # if keyword.isdigit(): 
            Member.bank.like('%' + more + '%'),
            # Member.iphone.like('%' + more  + '%'),
            Member.details.like('%' + more + '%'),
            ))
        
        # 单查
        if search:
            filters.append(Member.username.like('%' + search + '%'))


        # 盘口
        if ids:
            _ids = ids.split(',') or list[ids]
            filters.append(Member.handicap_id.in_(_ids))


        # 标签
        if tags:
            _tags = tags.split(',') or list[ids]
            filters.append(Member.tag)
            filters.append(Tag.id.in_(_tags))
        # 多对多关系链表查询: blog_list = Blog.query.filter(Blog.tags).filter(Tags.name.in_([tags])).order_by(desc("likes"))


        

        # -------------------------------------------------------------------------



        # -----------------------------  批量查询开始 ------------------------------
        batchSearch = xss_escape(request.args.get('batchsearch', type=str))
        if batchSearch:
            _many = batchSearch.split('\n') or list[batchSearch]
            filters.append(Member.username.in_(_many))

        # -------------------------------------------------------------------------





        # -----------------------------  多部门联合查询 ------------------------------

        # 如果用户属于某个部门，则过滤出某个部门资料
        if g.user.is_super:
            pass
        elif search or batchSearch or more:
            pass
        elif g.user.handicap_id:
            filters.append(Member.handicap_id==g.user.handicap_id)
        else:
            raise Forbidden(msg='权限不足')

        # -------------------------------------------------------------------------


        
        # obj = Member.query.filter(*filters).order_by(Member.create_at.desc()).layui_paginate()
        obj = Member.query.filter(Member.is_del==0).filter(*filters).order_by(Member.create_at.desc()).layui_paginate()
        count = obj.total
        return Success(data={'rows': model_to_dicts(schema=MemberOutSchema, data=obj.items), 'total': count})


class MemberAPIViews(views.MethodView):
    @authenticate(power='admin:member:show', log=False)
    def get(self, id):
        pass

    @authenticate(power='admin:member:add', log=True)
    def post(self):
        req_json = request.json
        tag_ids = req_json.get('tag_ids',[])
        username = xss_escape(req_json.get('username'))
        realname = xss_escape(req_json.get('realname'))
        bank = xss_escape(req_json.get('bank'))
        iphone = xss_escape(req_json.get('iphone'))
        details = xss_escape(req_json.get('details'))


        # 如果是超级管理员，则需要选择添加的部门，如果不是，则只添加到用户当前的部门
        if g.user.is_super:
            handicap_id = int(req_json.get('handicap_id'),0)
        else:
            handicap_id = g.user.handicap_id


        # 判断盘口是否存在
        is_hpExist = Handicap.query.get(handicap_id)
        if not is_hpExist:
            return ParameterException(msg="盘口不存在")
        
        # 判断当前盘口下的会员账号和添加的会员账号是否重复
        if Member.query.filter(and_(Member.username == username, Member.handicap_id == handicap_id)).first():
            raise ParameterException(msg="{0} 下 {1} 会员账号已经存在".format(is_hpExist.name,username))

        
        # 添加资料
        obj = Member(username=username, realname=realname, bank=bank, iphone=iphone,details=details,handicap_id=handicap_id)

        # 绑定标签
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        obj.tag = tags

        db.session.add(obj)
        db.session.commit()

        if not obj:
            raise ParameterException(msg='添加失败')
        return UpdateSuccess(msg="增加成功")

    @authenticate(power='admin:member:edit', log=True)
    def put(self, id):
        req = request.json
        _tagsLst = req.get("tagIds",[])
        tags = Tag.query.filter(Tag.id.in_(_tagsLst)).all()

        username = xss_escape(req.get("username"))
        realname = xss_escape(req.get("realname"))
        bank     = xss_escape(req.get("bank"))
        iphone   = xss_escape(req.get("iphone"))
        details  = xss_escape(req.get("details"))

        
        if g.user.is_super:
            obj = Member.query.get_or_404(id)
            obj.bank     = bank
            obj.iphone   = iphone
            obj.realname = realname
        else:
            obj = Member.query.filter(and_(Member.handicap_id==g.user.handicap_id, Member.id==id)).first()

        # # 先判断会员账号是否重复
        # is_exist = Member.query.filter_by(username=username).first()
        # if is_exist and is_exist.id != id:
        #     raise ParameterException(msg='{0} 此会员名已经存在'.format(username))


        obj.username = username
        obj.details  = details 
        # obj.handicap_id = int(req.get("handicapId"))
        obj.tag = tags


        

        db.session.commit()
        if not obj:
            raise ParameterException(msg="更新失败")
        return UpdateSuccess(msg="更新成功")
         

        
       

    @authenticate(power='admin:member:del', log=True)
    def delete(self, id):
        # obj = Member.query.filter_by(id=id).delete()
        if g.user.is_super:
            obj = Member.query.filter(Member.id==id)
        else:
            obj = Member.query.filter(and_(Member.id==id, Member.handicap_id==g.user.handicap_id))


        obj.update({'is_del': 1, 'delete_at': datetime.datetime.now()})
        db.session.commit()
        if not obj:
            raise ParameterException(msg="删除失败")
        return DeleteSuccess(msg="删除成功,已放入垃圾桶")






class MemberBatchAPIViews(views.MethodView):

    @authenticate(power='admin:member:batch:add', log=True)
    def post(self):
        req = request.json
        excels   = req.get('excel',None)

        
        # 定义初始化我们需要的数据
        initExcelData = {
                "会员账号": "username",
                "真实姓名": "realname",
                "银行卡号": "bank",
                # "联系电话": "iphone",
                "备注": "details",
                # "盘口": "handicap_id",
            }



        # query_handicap = Handicap.query.get_or_404(id)
        
        # 循环判断需要的中文字符是否存在于传进来的数据中
        if not excels:
            raise ParameterException(msg='无数据添加')
        for k,v in initExcelData.items():  
            is_exist = bool(map(lambda x: k in x, excels))
            if not is_exist:
                raise ParameterException(msg='{0}---格式不正确,请检查表头附近是否有空格或者格式不正确'.format(k))


        # 判断是否允许盘口添加, 如果 1 允许，并获取不在的盘口数据，并添加到数据库中
        # req_handicap = list(filter(None, list(set(map(lambda o: o['盘口'] , excels))))) # 某列去重，去空字符
        # _hLength = list(set(req_handicap).difference(set(handicapsList))) 
        # if checkboxes and '1' in checkboxes: 
        #     if len(_hLength) > 0:
        #         for i in _hLength:
        #             obj = Handicap()
        #             obj.name = i
        #             db.session.add(obj)
        #         # db.session.commit()
        # else:
        #     if len(_hLength) > 0:
        #         raise ParameterException(msg='存在不存在的盘口名字,如需要添加，请勾选允许添加不存在的盘口！')



        # 判断 EXCEL 添加的会员账户是否有重复， 如果是超级管理员,那么必须传入部门ID， 如果不是，则只添加到用户当前的部门
        # req_handicaps = list(set(map(lambda hId:hId['handicap'], excels)))
        
        if g.user.is_super:
            id = int(req.get('id')) # 条件
            query_handicap = Handicap.query.get_or_404(id)
            membersList = list(map(lambda o:o.username, Member.query.filter(Member.handicap_id==query_handicap.id).all()))
        else:
            # 不是超级管理员
            membersList = list(map(lambda o:o.username, Member.query.filter(Member.handicap_id==g.user.handicap_id).all()))


        req_member = list(filter(None, list(set(map(lambda o: o['会员账号'] , excels)))))
        if len(req_member) != len(excels):
            raise ParameterException(msg='请先剔除 EXCEL 中重复的会员账户')

        # 判断 数据库当中添加的会员账户是否有重复, 并集方式
        _mLength = list(set(req_member).intersection(set(membersList)))
        if len(_mLength) > 0:
            raise ParameterException(msg='{0} 会员账户已存在,请检查或者检查回收站'.format(','.join(_mLength)))

        data = []
        for d in excels:
            username    = d['会员账号']
            realname    = d['真实姓名']
            bank        = str(d['银行卡号'])
            # iphone      = str(d['联系电话'])
            details     = d['备注']

            data.append(              
                {
                    initExcelData['会员账号'] : username,
                    initExcelData['真实姓名'] : realname,
                    initExcelData['银行卡号'] : bank,
                    # initExcelData['联系电话'] : iphone,
                    initExcelData['备注'] : details,
                    'handicap_id' : query_handicap.id if g.user.is_super else g.user.handicap_id
                }
            )
            
        try:
            # start_time = datetime.datetime.utcnow()
            db.session.execute(
                Member.__table__.insert(),
                data
            )
            db.session.commit()
            # end_time = datetime.datetime.utcnow()
            # total = (end_time-start_time).total_seconds()
            return Success(msg='导入成功')
        except:
            raise ParameterException(msg='导入失败')

    @authenticate(power='admin:member:batch:edit', log=True)
    def put(self, ids=None):
        '''
            @批量更新一: 表格ID批量更新
            @批量更新二: 自定义会员号更新
        '''
        req = request.json
        _type        = int(xss_escape(req.get('type')))
        vips        = xss_escape(req.get('vips'))    # 自定义更新内容
        details     = xss_escape(req.get('details')) # 备注,value=0
        tag_ids     = req.get('tagIds', [])          # 标签,value=1
        handicap_id = req.get('handicapIds', 0)     # 盘口,value=2


        if ids:
            # 选中更新
            _ids_list = ids.split(',') or list[ids]
            obj = Member.query.filter(Member.id.in_(_ids_list))
        else:
            # 自定义更新
            _vips_list = vips.split('\n') or list[vips]

            # 如果是管理员，则需要选择更新的部门，否则只更新当前用户部门下的数据
            if g.user.is_super:
                obj = Member.query.filter(Member.handicap_id==handicap_id).filter(or_(Member.username.in_(_vips_list)))
            else:
                obj = Member.query.filter(Member.handicap_id==g.user.handicap_id).filter(or_(Member.username.in_(_vips_list)))

        if _type == 0:
            obj.update({'details': details})
        elif _type == 1:
            t = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            for o in obj.all():
                o.tag = t
        # elif _type == 2:
        #     obj.update({'handicap_id': int(handicap_id)})
        else:
            raise ParameterException(msg="未知更新")

        db.session.commit()
        if obj:
            return UpdateSuccess(msg="更新成功")
            
        return ServerError(msg="未知内部错误")

    @authenticate(power='admin:member:batch:del', log=True)
    def delete(self):
        req_json = request.json
        _ids= xss_escape(req_json.get('ids'))
        if not _ids:
            raise ParameterException(msg="无效数据")
        _idsList = _ids.split(',') or list[_ids]

        # 如果是超级管理员，则可以直接删除，否则只允许当前部门用户删除
        if g.user.is_super:
            obj = Member.query.filter(Member.id.in_(_idsList))
        else:
            obj = Member.query.filter(Member.handicap_id==g.user.handicap_id).filter(Member.id.in_(_idsList))

        obj.update({'is_del': 1, 'delete_at': datetime.datetime.now()})
        db.session.commit()

        if obj:
            return DeleteSuccess(msg="删除成功,已放入垃圾桶")
        return ServerError(msg="未知内部错误")


class MemberRecoveryAPIViews(views.MethodView):

    @authenticate(power='admin:member:recovery', log=False)
    def get(self):
        search = xss_escape(request.args.get('search', type=str))

        mf = ModelFilter()

        if search:
            mf.vague(field_name="username", value=search)

        obj = Member.query.filter(Member.is_del==1).filter(mf.get_filter(Member)).order_by(Member.delete_at.desc()).layui_paginate()
        count = obj.total
        return Success(data={'rows': model_to_dicts(schema=MemberOutSchema, data=obj.items), 'total': count})


    @authenticate(power='admin:member:recovery', log=True)
    def put(self):
        req_json = request.json
        _ids= xss_escape(req_json.get('ids'))
        if not _ids:
            raise ParameterException(msg="无效数据")
        _idsList = _ids.split(',') or list[_ids]


        if g.user.is_super:
            obj = Member.query.filter(Member.id.in_(_idsList)).update({'is_del': 0 })
        else:
            obj = Member.query.filter(Member.handicap_id==g.user.handicap_id).filter(Member.id.in_(_idsList)).update({'is_del': 0 })

        # obj = Member.query.filter(Member.id.in_(_idsList)).update({'is_del': 0 })
        db.session.commit()

        if obj:
            return DeleteSuccess(msg="数据已还原")
        return ServerError(msg="未知内部错误")


    @authenticate(power='admin:member:recovery', log=True)
    def delete(self):
        req_json = request.json
        _ids= xss_escape(req_json.get('ids'))

        if not _ids:
            raise ParameterException(msg="无效数据")
            
        _idsList = _ids.split(',') or list[_ids]

        if g.user.is_super:
            obj = Member.query.filter(Member.id.in_(_idsList)).delete()
        else:
            obj = Member.query.filter(Member.handicap_id==g.user.handicap_id).filter(Member.id.in_(_idsList)).delete()


        # obj = Member.query.filter(Member.id.in_(_idsList)).delete()
        db.session.commit()

        if obj:
            return DeleteSuccess(msg="删除成功,已永久删除")
        return ServerError(msg="未知内部错误")
    


admin_member.add_url_rule('/member/temp',            view_func=MemberTempAPIViews.as_view('memberTemp'),         endpoint='memberTemp',     methods=['GET'])        # 模板
admin_member.add_url_rule('/member/list',            view_func=MemberListAPIViews.as_view('memberList'),         endpoint='memberList',     methods=['GET'])        # 列表
admin_member.add_url_rule('/member/<int:id>',        view_func=MemberAPIViews.as_view('member'),                 endpoint='member',         methods=['GET','PUT','DELETE']) # 查改删
admin_member.add_url_rule('/member',                 view_func=MemberAPIViews.as_view('memberAdd'),              endpoint='memberAdd',      methods=['POST'])                  # 增
admin_member.add_url_rule('/member/batch',           view_func=MemberBatchAPIViews.as_view('memberBatch'),       endpoint='memberBatch',    methods=['PUT','POST','DELETE'])     # 批量增，修，删
admin_member.add_url_rule('/member/batch/<ids>',     view_func=MemberBatchAPIViews.as_view('memberBatchTwo'),    endpoint='memberBatchTwo',    methods=['PUT'])                  # 表格方式批量修改


admin_member.add_url_rule('/member/recovery',        view_func=MemberRecoveryAPIViews.as_view('memberRecovery'), endpoint='memberRecovery',     methods=['GET','PUT','DELETE'])        # 列表



from flask import Response

@admin_member.route("/member/<path:filename>")
@authenticate()
def downloadFile(filename):
    import os
    # baseDir = os.path.join(os.getcwd(), "static")
    # pathname = os.path.join(baseDir, filename)
    baseDir = os.path.abspath(os.path.dirname(__file__)).split('applications')[0]
    pathname = os.path.join(baseDir, "static/public/" + filename)
    def send_chunk():  # 流式读取
        store_path = pathname
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)  # 每次读取20M
                if not chunk:
                    break
                yield chunk


    # response = Response(send_chunk(), content_type='application/gzip') # 下载压缩包
    response = Response(send_chunk(), content_type='application/octet-stream')
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    response.headers['content-length'] = os.stat(str(pathname)).st_size  # 文件总大小
    return response