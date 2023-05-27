from applications.extensions import ma
from applications.common.utils.hide import fHideMid
from marshmallow import fields,post_dump
from applications.models import Handicap
from flask import g

# from marshmallow_sqlalchemy import  SQLAlchemyAutoSchema

class TagOutSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    color = fields.Str(required=True)
    create_at = fields.DateTime(dump_only=True)
    update_at = fields.DateTime(dump_only=True)
    handicap = fields.Method("get_handicap")

    def get_handicap(self, obj):
        if obj.handicap_id != None:
            d = Handicap.query.filter_by(id=obj.handicap_id).first()
            return {'id': d.id, 'name': d.name }
        else:
            return None


# class MemberOutSchema(ma.Schema):
class MemberOutSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    realname = fields.Str(required=True)
    bank = fields.Str(required=True)
    # iphone = fields.Str(required=True)
    # tag = fields.Str()
    details = fields.Str()
    is_del = fields.Integer(dump_only=True)
    create_at = fields.DateTime(dump_only=True)
    update_at = fields.DateTime(dump_only=True)
    delete_at = fields.DateTime()
    handicap = fields.Method("get_handicap")

    tag = fields.List(fields.Nested(lambda: TagOutSchema(only=("id", "name","color"))))

    # class Meta:
    #     model = Handicap       # 关联模型
    #     include_fk = True


    def get_handicap(self, obj):
        if obj.handicap_id != None:
            d = Handicap.query.get(int(obj.handicap_id))
            if d:
                return {'id': d.id, 'name': d.name }
            else:
                return None
        else:
            return None


    @post_dump
    def post_dump(self,data,**kwargs):
        """序列化钩子方法"""
        if not g.user.is_super:
            # data["realname"] = fHideMid(data['realname'], count=1)
            data["bank"] = fHideMid(data['bank'], count=8)
            # data["iphone"] = fHideMid(data['iphone'], count=3)
            # data["iphone"] = data["mobile"][:3]+"****"+data["mobile"][-4:]
            return data
        return data
