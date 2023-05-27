from flask import Blueprint, views,g,request,make_response
from applications.common.utils.http import Success,ParameterException,NotFound,DeleteSuccess,ServerError
from applications.common.utils.rights import authenticate
from applications.models.other.admin_title import Title
from applications.jsonp.other.jsonp_title import getTitleJson
from applications.common.curd import model_to_dicts
from applications.common.utils.validate import xss_escape
from applications.common.tasks.tasks import BatchGetTitle
from applications.schemas import TitleOutSchema,WeightOutSchema
from applications.extensions import db
from sqlalchemy import or_,and_
import time
import os
from io import BytesIO



admin_title = Blueprint('adminTitle', __name__)


class TitleTempAPIViews(views.MethodView):
    @authenticate(power='admin:title', log=False)
    def get(self):
        data = getTitleJson(g.permissions)
        return Success(data=data)

class TitleListAPIViews(views.MethodView):

    @authenticate(power='admin:title:list', log=False)
    def get(self):
        # 获取请求参数
        tag = xss_escape(request.args.get('tag', type=str))
        upload_tag = xss_escape(request.args.get('upload_tag', type=str))
        status = xss_escape(request.args.get('status', type=str))
        search = xss_escape(request.args.get('search', type=str))
        more = xss_escape(request.args.get('more', type=str))
        daytime = xss_escape(request.args.get('daytime', type=str))
        weight = xss_escape(request.args.get('weight', type=str))
        # donwloadType  = xss_escape(request.args.get('daytime', type=str))
        
        # if donwloadType == '2':
        #     Title.query.all()



        # -----------------------------  多条件查询开始 ----------------------------
        filters = []

        # 权重
        if weight:
            # filters.append(Title.weight == weight)
            wt = weight.split(',') or list[weight]
            filters.append(or_(
                Title.weight == w for w in wt
            ))


        # 标签
        if tag:
            filters.append(Title.tag == tag)

        # 导入上传标签
        if upload_tag:
            tg = upload_tag.split(',') or list[upload_tag]
            filters.append(or_(
                Title.upload_tag == t for t in tg
            ))
            # filters.append(Title.upload_tag == upload_tag)

        # 状态
        if status:
            filters.append(Title.status == int(status))
        
        # 多查
        if more:
            mr = more.split(',') or list[more]
            filters.append(or_(
                # Title.title.like('%' + more + '%'),
                # Title.keywords.like('%' + more + '%'),
                Title.description.like('%' + t + '%') for t in mr

            ))


        
        # 单查
        if search:
            filters.append(Title.url.like('%' + search + '%'))

        # 日期时间范围
        if daytime:
            _daytime = daytime.split(',')
            filters.append(and_(Title.create_time >= _daytime[0],Title.create_time <= _daytime[1]))
            

        # -------------------------------------------------------------------------


        # -----------------------------  批量查询开始 ------------------------------
        batchSearch = xss_escape(request.args.get('batchsearch', type=str))
        if batchSearch:
            _many = batchSearch.split('\n') or list[batchSearch]
            filters.append(Title.url.in_(_many))

        # -------------------------------------------------------------------------


        # mf.exact(field_name="type", value=0)
        # orm查询
        # 使用分页获取data需要.items
        # obj = Power.query.filter(mf.get_filter(model=Power)).layui_paginate()
        obj = Title.query.filter(*filters).order_by(Title.create_time.desc()).layui_paginate()
        count = obj.total
        rows = model_to_dicts(schema=TitleOutSchema, data=obj.items)
        return Success(data={'rows': rows, 'total': count})

    @authenticate(power='admin:title:batch:add', log=True)
    def post(self):
        from datetime import date
        req = request.json
        excels   = req.get('excel',None)
        upload_tag = req.get('uploadTag',date.today().strftime("%Y-%m-%d"))

        # 定义初始化我们需要的数据
        initExcelData = {
                "网址域名": "url",
                "权重": 'weight'
            }
         # 循环判断需要的中文字符是否存在于传进来的数据中
        if not excels:
            raise ParameterException(msg='无数据添加')
        for k,v in initExcelData.items():  
            is_exist = bool(map(lambda x: k == x, excels))
            if not is_exist:
                raise ParameterException(msg='{0}---格式不正确,请检查表头附近是否有空格或者格式不正确'.format(k))

        # 判断 数据库当中添加的会员账户是否有重复, 并集方式
        # titlesList = list(map(lambda o:o.url, Title.query.all()))
        # req_title = list(filter(None, list(set(map(lambda o: o['网址域名'] , excels)))))
        # if len(req_title) != len(excels):
        #     raise ParameterException(msg='请先剔除 EXCEL 中重复的网址域名')

        # _mLength = list(set(req_title).intersection(set(titlesList)))
        # if len(_mLength) > 0:
        #     raise ParameterException(msg='{0} 网址域名已存在,请检查'.format(','.join(_mLength)))

        data = []
        for d in excels:
            url    = d['网址域名']
            weight = d['权重'] or 0
            data.append(              
                {
                    initExcelData['网址域名'] : url,
                    initExcelData['权重'] : weight,
                    'upload_tag': upload_tag,
                }
            )
        try:
            db.session.execute(
                Title.__table__.insert(),
                data
            )
            db.session.commit()
            return Success(msg='导入成功')
        except:
            raise ParameterException(msg='导入失败')
                

    @authenticate(power='admin:title:batch:edit', log=True)
    def put(self):
        req = request.json
        ids = req['ids']
        _ids = ids.split(',') or list(ids)
        
        title = Title.query.filter(Title.id.in_(_ids)).update({'status': 0})
        # title = Title.query.filter(or_(Title.tag=="无法访问",Title.tag=="无标题",Title.tag=="访问错误")).update({'status': 0})
        db.session.commit()
        if title:
            return Success(msg="提交执行查询任务成功")
        return ParameterException(msg="提交执行查询任务失败")

        

    @authenticate(power="admin:title:batch:del", log=True)
    def delete(self):
        req = request.json
        ids = req['ids']
        _ids = ids.split(',') or list(ids)
        title = Title.query.filter(Title.id.in_(_ids)).delete(synchronize_session=False)
        db.session.commit()
        if title:
            return Success(msg="删除成功")
        else:
            return ParameterException(msg="删除失败")

class TitleAPIViews(views.MethodView):
    @authenticate("admin:title:show", log=True)
    def get(self):
        pass

    @authenticate("admin:title:add", log=True)
    def post(self):
        req = request.json
        url = xss_escape(req.get("url"))

        # q = Title.query.filter_by(url=url).first()
        # if q:
        #     raise ParameterException(msg='{0} 已存在'.format(url))

        obj = Title(
            url    = url,
        )
        db.session.add(obj)
        db.session.commit()
        if obj:
            return Success(msg="添加成功")
        return ParameterException(msg='添加失败')

    @authenticate("admin:title:edit", log=True)
    def put(self,id):
        res = Title.query.filter_by(id=id)
        if not res:
            raise NotFound()
        stdout = BatchGetTitle([{'id': res.first().id, 'url': res.first().url}])
        r = stdout.url_main()
        # r = stdout.sdk_main()
        

        res.update(r[0])

        db.session.commit()
        if not res:
            raise ParameterException(msg='查询失败')
        return Success(msg='查询成功')



    @authenticate("admin:title:del", log=True)
    def delete(self,id):
        # _id = request.form.get('id')
        res = Title.query.filter_by(id=id)
        if not res:
            raise NotFound()

        res.delete()
        db.session.commit()
        if res:
            return Success(msg="删除成功")
        else:
            return ParameterException(msg="删除失败")





admin_title.add_url_rule('/title/temp', view_func=TitleTempAPIViews.as_view('titleTemp'), endpoint='titleTemp', methods=['GET'])        # 模板
admin_title.add_url_rule('/title/list', view_func=TitleListAPIViews.as_view('titleList'), endpoint='titleList', methods=['GET'])        # 列表
admin_title.add_url_rule('/title/batch',       view_func=TitleListAPIViews.as_view('titleBatchAdd'), endpoint='titleBatchAdd', methods=['POST','PUT','DELETE'])        # 批量添加
# admin_title.add_url_rule('/title/batch/<ids>', view_func=TitleListAPIViews.as_view('titleBatchDel'), endpoint='titleBatchDel', methods=['DELETE'])        # 列表
admin_title.add_url_rule('/title/<int:id>',    view_func=TitleAPIViews.as_view('title'), endpoint='title', methods=['GET','PUT','DELETE']) # 查改删
admin_title.add_url_rule('/title',             view_func=TitleAPIViews.as_view('addtitle'), endpoint='addtitle', methods=['POST'])                  # 增




from flask import Response

@admin_title.route("/title/<path:filename>")
@authenticate()
def downloadFile(filename):
    
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



@admin_title.route("/title/all")
@authenticate(power='admin:title:list')
def downloadTitleAll():
    # -----------------------------  多条件查询开始 ----------------------------
    tag = xss_escape(request.args.get('tag', type=str))
    status = xss_escape(request.args.get('status', type=str))
    search = xss_escape(request.args.get('search', type=str))
    more = xss_escape(request.args.get('more', type=str))
    daytime = xss_escape(request.args.get('daytime', type=str))
    upload_tag = xss_escape(request.args.get('upload_tag', type=str))
    # donwloadType  = xss_escape(request.args.get('daytime', type=str))

    filters = []

    # 标签
    if tag:
        filters.append(Title.tag == tag)

    if upload_tag:
            tg = upload_tag.split(',') or list[upload_tag]
            filters.append(or_(
                Title.upload_tag == t for t in tg
            ))
            
    # 状态
    if status:
        filters.append(Title.status == int(status))
    
    # 多查
    if more:
        mr = more.split(',') or list[more]
        filters.append(or_(
            Title.description.like('%' + m + '%') for m in mr
        ))
    
    # 单查
    if search:
        filters.append(Title.url.like('%' + search + '%'))

    # 日期时间范围
    if daytime:
        _daytime = daytime.split(',')
        filters.append(and_(Title.create_time >= _daytime[0],Title.create_time <= _daytime[1]))
        

    # -------------------------------------------------------------------------


    obj = Title.query.filter(*filters).order_by(Title.create_time.desc()).all()
    # rows = model_to_dicts(schema=TitleOutSchema, data=obj)

    # rows = [{'id': 1, 'tag': 2, 'title': 3, 'status':4, 'title': 5}]
    # 循环写入数据到文件
    import xlwt
    ws = xlwt.Workbook(encoding='utf-8')
    
    sheet = 1
    n = 0
    while 0 > -1:
        d = obj[n:n+65534]
        if not d:
            break
        
        # al = xlwt.Alignment()
        # al.horz = 0x02 # 居中
        # style = xlwt.XFStyle() # 初始化样式
        # style.alignment = al


        st = ws.add_sheet(f'表{sheet}')
        # 写标题行
        st.write(0, 0, '权重')
        st.write(0, 1, '网址域名')
        st.write(0, 2, '网址标题')
        st.write(0, 3, '网址关键词')
        # st.write(0, 4, '网址描述')
        st.write(0, 4, '上传标签')
        st.write(0, 5, '爬虫标签')
        st.write(0, 6, '查询状态')
        st.write(0, 7, '创建时间')
        st.write(0, 8, '更新时间')
        # 写入数据，从第一行开始 
        excel_row = 1
        _status = {'0': '未查询', '1': '已查询', '2': '待查询', '3':'准备抓取域名页面', '4':"待站长二次查询"}
        for o in d:
            st.write(excel_row, 0, o.weight)
            st.write(excel_row, 1, o.url)
            st.write(excel_row, 2, o.title)
            st.write(excel_row, 3, o.keywords)
            # st.write(excel_row, 4, o.description)
            st.write(excel_row, 4, o.upload_tag)
            st.write(excel_row, 5, o.tag)
            st.write(excel_row, 6, _status[str(o.status)] )
            st.write(excel_row, 7, str(o.create_time))
            st.write(excel_row, 8, str(o.update_time))
            excel_row += 1

        n = n + 65534
        sheet = sheet + 1

    output = BytesIO()
    ws.save(output)
    output.seek(0)
    # -----------------------------------------------------
    # # 创建IO对象
    # output = BytesIO()
    # # 写excel
    # workbook = xlsxwriter.Workbook(output)  # 先创建一个book，直接写到io中

    # sheet = workbook.add_worksheet('sheet1')
    # fileds = ['create_time', 'update_time', 'id', 'status','tag','title']

    # # 写入数据到A1一列
    # sheet.write_row('A1', fileds)

    # # 遍历有多少行数据
    # for i in range(len(rows)):
    #     # 遍历有多少列数据
    #     for x in range(len(fileds)):
    #         key = [key for key in rows[i].keys()]
    #         sheet.write(i + 1, x, rows[i][key[x]])
    #         # current_app.logger.info('当前行：{}  当前列：{}  数据：{}'.format(str(i), str(x), data[i][key[x]]))
    # workbook.close()  # 需要关闭
    # output.seek(0)  # 找到流的起始位置
    # -----------------------------------------------------

    resp = make_response(output.getvalue())
    filename = time.strftime("%Y-%m-%d", time.localtime())
    basename = f'{filename}.xlsx'

    # 转码，支持中文名称
    resp.headers["Content-Disposition"] = f"attachment; filename={basename}"
    resp.headers['Content-Type'] = 'application/vnd.ms-excel'
    resp.headers["Cache-Control"] = "no_store"
    return resp


    
    # response = Response(send_chunk(), content_type='application/octet-stream')
    # response.headers['Content-Type'] = 'application/xlsx'
    response.headers['Content-Type'] = mime_type
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    response.headers['content-length'] = os.stat(str(pathname)).st_size  # 文件总大小
    return response
    return Success(msg='success')
    # return Success(data={'rows': rows, 'total': len(obj)})

@admin_title.route("/title/weight")
@authenticate(power='admin:title:list')
def getTitleWeight():
    obj  = Title.query.with_entities(Title.weight).distinct()
    rows = model_to_dicts(schema=TitleOutSchema, data=obj.all())
    for r in rows:
        r['label'] = "权重 %s" % r['weight']
    return Success(data={'rows': rows, 'total': obj.count()})


@admin_title.route("/title/tag")
@authenticate(power='admin:title:list')
def getTitleTag():
    obj  = Title.query.with_entities(Title.tag).distinct()
    rows = model_to_dicts(schema=TitleOutSchema, data=obj.all())
    for r in rows:
        r['label'] = "%s" % r['tag']
    return Success(data={'rows': rows, 'total': obj.count()})

@admin_title.route("/title/upload_tag")
@authenticate(power='admin:title:list')
def getTitleUploadTag():
    obj  = Title.query.with_entities(Title.upload_tag).distinct()
    rows = model_to_dicts(schema=TitleOutSchema, data=obj.all())
    for r in rows:
        r['label'] = "%s" % r['upload_tag']
    return Success(data={'rows': rows, 'total': obj.count()})



@admin_title.delete("/title/truncate")
@authenticate(power='admin:title:batch:truncate',log=True)
def delTitleAll():
    try:
        db.get_engine().execute(f"truncate table admin_title")
        return DeleteSuccess(msg='清空表成功')
    except:
        return ServerError(msg='内部错误')
    # from sqlalchemy.ext.declarative import declarative_base
    # Base = declarative_base()

    # obj = db.session.execute(
    #     Base.metadata.tables['admin_title'].delete()
    # )
    # db.session.commit()
    # if not obj:
    #     return ServerError(msg='清空表失败')
    


@admin_title.get("/title/roll")
def roll():
    Title.query.filter_by(tag='获取站长数据失败').update({'status': 0})
    db.session.commit()
    return Success()

# # 图片批量删除
# @admin_file.route('/batchRemove', methods=['GET', 'POST'])
# @authorize("admin:file:delete", log=True)
# def batch_remove():
#     ids = request.form.getlist('ids[]')
#     title_name = Title.query.filter(Title.id.in_(ids)).all()
#     upload_url = current_app.config.get("UPLOADED_PHOTOS_DEST")
#     for p in title_name:
#         os.remove(upload_url + '/' + p.name)
#     title = Title.query.filter(Title.id.in_(ids)).delete(synchronize_session=False)
#     db.session.commit()
#     if title:
#         return success_api(msg="删除成功")
#     else:
#         return fail_api(msg="删除失败")