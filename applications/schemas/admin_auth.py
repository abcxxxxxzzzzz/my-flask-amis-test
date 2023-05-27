from applications.extensions import ma
from marshmallow import fields


class LoginSchema(ma.Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)