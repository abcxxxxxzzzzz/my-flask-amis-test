from applications.extensions import ma
from marshmallow import fields, post_dump


# 权限models序列化类
class PowerOutSchema(ma.Schema):
    id = fields.Integer()
    name = fields.Str()
    type = fields.Str()
    code = fields.Str()
    url = fields.Str()
    # schema_url = fields.Str()
    open_type = fields.Str()
    parent_id = fields.Integer()
    icon = fields.Str()
    sort = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
    enable = fields.Integer()
    # children = fields.List(fields.Nested(lambda: PowerOutSchema), attribute="parent")
    # children = fields.List(fields.Nested(lambda: PowerOutSchema(only=("id",))), attribute="parent")

    # @post_dump
    # def post_dump(self,data,**kwargs):
    #     print(data)
    #     return data



class PowerOutSchema2(ma.Schema):  # 序列化类
    id = fields.Integer()
    label = fields.Str(attribute='name')
    parent_id = fields.Integer()
    sort = fields.Integer()
    

    @post_dump
    def post_dump(self,data,**kwargs):
        # print(data)
        data['value'] = data['id']
        return data
