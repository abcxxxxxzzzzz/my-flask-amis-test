
import datetime
from applications.extensions import db




# 组
class Handicap(db.Model):
    __tablename__ = 'admin_handicap'
    id = db.Column(db.Integer, unique=True,primary_key=True, comment='盘口ID')
    name = db.Column(db.String(255), index=True, unique=True,comment='盘口名称')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')


    # 关联会员
    relate_member = db.relationship("Member", backref='relate_handicap', lazy='dynamic')

    # 关联用户
    relate_user = db.relationship("User", backref='relate_user', lazy='dynamic')

    # 关联标签
    relate_user = db.relationship("Tag", backref='relate_tag', lazy='dynamic')

    # 关联https ssl 域名
    relate_https = db.relationship("HTTPSDomain", backref='relate_https', lazy='dynamic')