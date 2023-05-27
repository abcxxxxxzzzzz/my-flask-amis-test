from flask import Blueprint, views,g,request,current_app
from applications.common.utils.http import Success,ParameterException
from applications.common.utils.rights import authenticate
from applications.common.utils import upload as upload_curd
from applications.models.admin_photo import Photo
from applications.jsonp.rbac.jsonp_photo import getPhotoJson
from applications.common.curd import model_to_dicts
from applications.common.utils.validate import xss_escape
from applications.common.helper import ModelFilter
from applications.schemas import PhotoOutSchema
from applications.extensions import db
import os


admin_photo = Blueprint('adminPhoto', __name__)


class PhotoTempAPIViews(views.MethodView):
    @authenticate(power='admin:photo', log=False)
    def get(self):
        data = getPhotoJson(g.permissions)
        return Success(data=data)

class PhotoListAPIViews(views.MethodView):

    @authenticate(power='admin:photo:list', log=False)
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
        obj = Photo.query.filter(mf.get_filter(model=Photo)).layui_paginate()
        count = obj.total
        rows = model_to_dicts(schema=PhotoOutSchema, data=obj.items)
        return Success(data={'rows': rows, 'total': count})

    @authenticate(power="admin:photo:batch:del", log=True)
    def delete(self,ids):
        _ids = ids.split(',') or list(ids)
        photo_name = Photo.query.filter(Photo.id.in_(_ids)).all()
        upload_url = current_app.config.get("UPLOADED_PHOTOS_DEST")
        for p in photo_name:
            try:
                os.remove(upload_url + '/' + p.name)
            except:
                continue
        photo = Photo.query.filter(Photo.id.in_(_ids)).delete(synchronize_session=False)
        db.session.commit()
        if photo:
            return Success(msg="删除成功")
        else:
            return ParameterException(msg="删除失败")

class PhotoAPIViews(views.MethodView):
    @authenticate("admin:photo:show", log=True)
    def get(self):
        pass

    @authenticate("admin:photo:add", log=True)
    def post(self):
        if 'file' in request.files:
            photo = request.files['file']
            mime = request.files['file'].content_type

            file_url = upload_curd.upload_one(photo=photo, mime=mime)
            return Success(msg="上传成功",data={"value": file_url})
        return ParameterException(msg="上传失败")

    @authenticate("admin:photo:edit", log=True)
    def put(self):
        pass

    @authenticate("admin:photo:del", log=True)
    def delete(self,id):
        # _id = request.form.get('id')
        res = upload_curd.delete_photo_by_id(id)
        if res:
            return Success(msg="删除成功")
        else:
            return ParameterException(msg="删除失败")


admin_photo.add_url_rule('/photo/temp', view_func=PhotoTempAPIViews.as_view('photoTemp'), endpoint='photoTemp', methods=['GET'])        # 模板
admin_photo.add_url_rule('/photo/list', view_func=PhotoListAPIViews.as_view('photoList'), endpoint='photoList', methods=['GET'])        # 列表
admin_photo.add_url_rule('/photo/batch/<ids>', view_func=PhotoListAPIViews.as_view('photoBatchDel'), endpoint='photoBatchDel', methods=['delete'])        # 列表
admin_photo.add_url_rule('/photo/<int:id>', view_func=PhotoAPIViews.as_view('photo'), endpoint='photo', methods=['GET','PUT','DELETE']) # 查改删
admin_photo.add_url_rule('/photo', view_func=PhotoAPIViews.as_view('addphoto'), endpoint='addphoto', methods=['POST'])                  # 增








# # 图片批量删除
# @admin_file.route('/batchRemove', methods=['GET', 'POST'])
# @authorize("admin:file:delete", log=True)
# def batch_remove():
#     ids = request.form.getlist('ids[]')
#     photo_name = Photo.query.filter(Photo.id.in_(ids)).all()
#     upload_url = current_app.config.get("UPLOADED_PHOTOS_DEST")
#     for p in photo_name:
#         os.remove(upload_url + '/' + p.name)
#     photo = Photo.query.filter(Photo.id.in_(ids)).delete(synchronize_session=False)
#     db.session.commit()
#     if photo:
#         return success_api(msg="删除成功")
#     else:
#         return fail_api(msg="删除失败")