from applications.extensions import ma
from marshmallow import fields,post_dump
from applications.models import Handicap



class HTTPSDomainOutSchema(ma.Schema):
    id          = fields.Integer()
    name        = fields.Str()
    expir_day   = fields.Integer()
    enable      = fields.Integer()
    remark      = fields.Str()
    create_at = fields.DateTime()
    update_at = fields.DateTime()


    handicap = fields.Method("get_handicap")

    def get_handicap(self, obj):
        if obj.handicap_id != None:
            d = Handicap.query.get(int(obj.handicap_id))
            if d:
                return {'id': d.id, 'name': d.name }
            else:
                return None
        else:
            return None




