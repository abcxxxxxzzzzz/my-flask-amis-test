from applications.extensions import ma
from marshmallow import fields
from .admin_role import RoleOutSchema
from applications.models import Handicap

# 用户models的序列化类
class UserOutSchema(ma.Schema):
    id = fields.Integer()
    username = fields.Str()
    realname = fields.Str()
    enable = fields.Integer()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    role = fields.List(fields.Nested(lambda: RoleOutSchema(only=("id", "roleName"))))

    # from applications.schemas.live.admin_handicap import HandicapOutSchema
    # handicap = fields.List(fields.Nested(lambda: HandicapOutSchema(only=("id", "name"))))
    handicap = fields.Method("get_handicap")
    is_super = fields.Integer()
    
    def get_handicap(self, obj):
        if obj.handicap_id != None:
            d = Handicap.query.filter_by(id=obj.handicap_id).first()
            return {'id': d.id, 'name': d.name }
        else:
            return None

    # dept = fields.Method("get_dept")

    # def get_dept(self, obj):
    #     if obj.dept_id != None:
    #         return Dept.query.filter_by(id=obj.dept_id).first().dept_name
    #     else:
    #         return None