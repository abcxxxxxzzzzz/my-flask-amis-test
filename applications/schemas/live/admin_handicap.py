from applications.extensions import ma
from marshmallow import fields



class HandicapOutSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    create_at = fields.DateTime(dump_only=True)
    update_at = fields.DateTime(dump_only=True)