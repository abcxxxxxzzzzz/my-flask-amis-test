from applications.models import Handicap
from  applications.extensions import db
import datetime




# 会员标签
class HTTPSDomain(db.Model):
    __tablename__ = 'admin_domain_https'
    id = db.Column(db.Integer, unique=True, primary_key=True, comment='域名ID')
    name      = db.Column(db.String(255), index=True,comment='域名名称')
    expir_day = db.Column(db.Integer, index=True,comment='到期时间')
    enable    = db.Column(db.Integer, default=0, comment='是否检测')
    remark = db.Column(db.String(255), comment='备注')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='添加时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')

    # 所属组
    handicap_id = db.Column(db.Integer, db.ForeignKey('admin_handicap.id'))
