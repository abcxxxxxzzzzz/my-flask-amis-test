import datetime
from applications.extensions import db



class Title(db.Model):
    __tablename__ = 'admin_title'
    id     = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    url    = db.Column(db.String(255), index=True, comment="网址")
    title  = db.Column(db.Text(), comment="网站标题")
    keywords = db.Column(db.Text(), comment="网站关键词")
    description = db.Column(db.Text(), comment="网站描述")
    upload_tag = db.Column(db.String(255), index=True, comment="上传标签")
    tag    = db.Column(db.String(255), index=True,comment="爬虫标签")
    status = db.Column(db.Integer, index=True,default=0, comment='状态')
    weight = db.Column(db.Integer, index=True,default=0, comment='权重')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
