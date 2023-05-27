from applications.extensions import ma
from marshmallow import fields,post_dump

class TitleOutSchema(ma.Schema):
    id     = fields.Integer()
    url    = fields.Str()
    title  = fields.Str()
    keywords  = fields.Str()
    description  = fields.Str()
    upload_tag    = fields.Str()
    tag    = fields.Str()
    status = fields.Integer()
    weight = fields.Integer() 
    create_time = fields.DateTime()
    update_time = fields.DateTime()



class WeightOutSchema(ma.Schema):
    # id     = fields.Integer()
    weight = fields.Integer() 
    # label = fields.Method("get_label")


    # def get_label(self, obj):
    #     if obj.weight != None:
    #         return '权重' + str(obj.weight)
    #     else:
    #         return '无'

    # @post_dump
    # def post_dump(self,data,**kwargs):
    #     """序列化钩子方法"""
    #     if data['weight'] is not None:
    #         data["label"] = '权重' + str(data['weight'])
    #         return data
    #     # data["iphone"] = fHideMid(data['iphone'], count=3)
    #     # data["iphone"] = data["mobile"][:3]+"****"+data["mobile"][-4:]
    #     data["label"] = '空'
    #     return data