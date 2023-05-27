from applications.extensions import ma
from marshmallow import fields
from .admin_power import PowerOutSchema


class RoleOutSchema(ma.Schema):
    id = fields.Integer()
    roleName = fields.Str(attribute="name")
    roleCode = fields.Str(attribute="code")
    enable = fields.Str()
    # remark = fields.Str()
    details = fields.Str()
    sort = fields.Integer()
    create_at = fields.DateTime(attribute="create_time")
    update_at = fields.DateTime(attribute="update_time")
    power = fields.List(fields.Nested(lambda: PowerOutSchema(only=("id", "name"))))
