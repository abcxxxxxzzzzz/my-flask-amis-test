import datetime
from applications.extensions import db
from .admin_handicap import Handicap



# 创建中间表
member_tag = db.Table(
    "admin_member_tag",  # 中间表名称
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    db.Column("member_id", db.Integer,  db.ForeignKey("admin_member.id", ondelete="CASCADE", onupdate="CASCADE"), index=True, comment='会员编号'),  # 属性 外键
    db.Column("tag_id", db.Integer, db.ForeignKey("admin_tag.id", ondelete="CASCADE", onupdate="CASCADE"),index=True, comment='标签编号'),  # 属性 外键
)


# 会员标签
class Tag(db.Model):
    __tablename__ = 'admin_tag'
    id = db.Column(db.Integer, unique=True, primary_key=True, comment='标签ID')
    name  = db.Column(db.String(255), index=True,comment='标签名称')
    color = db.Column(db.String(255), comment='标签颜色')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='添加时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')

    # 所属组
    handicap_id = db.Column(db.Integer, db.ForeignKey('admin_handicap.id'))

# 会员资料
class Member(db.Model):
    __tablename__ = 'admin_member'
    id = db.Column(db.Integer, unique=True,primary_key=True, autoincrement=True, comment='会员ID')
    username = db.Column(db.String(255),index=True, comment='会员账户')
    realname = db.Column(db.String(255), index=True,comment='真实姓名')
    bank = db.Column(db.String(255), index=True,comment='绑定银行卡')
    # tag = db.Column(db.String(255), comment='彩金标签')
    iphone = db.Column(db.String(20),index=True, comment='联系电话')
    details = db.Column(db.String(255), index=True,comment='备注')
    is_del = db.Column(db.Integer, default=0, comment='是否已删除')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='添加时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    delete_at = db.Column(db.DateTime, comment='删除时间')
    handicap_id = db.Column(db.Integer, db.ForeignKey('admin_handicap.id'))

    tag = db.relationship('Tag', secondary="admin_member_tag", backref=db.backref('member'), lazy='dynamic')


