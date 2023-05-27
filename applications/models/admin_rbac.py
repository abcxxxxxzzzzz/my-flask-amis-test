import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from applications.extensions import db, Redis
from applications.common.utils.http import AuthFailed,NotFound
from itsdangerous import BadSignature, SignatureExpired, TimedJSONWebSignatureSerializer
from flask import current_app


# 用户表
class User(db.Model, UserMixin):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(20), comment='用户名')
    realname = db.Column(db.String(20), comment='真实名字')
    avatar = db.Column(db.String(255), comment='头像', default="/static/admin/admin/images/avatar.jpg")
    remark = db.Column(db.String(255), comment='备注')
    password_hash = db.Column(db.String(128), comment='哈希密码')
    enable = db.Column(db.Integer, default=0, comment='启用')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    role = db.relationship('Role', secondary="admin_user_role", backref=db.backref('user'), lazy='dynamic')

    ## 添加多个部门组
    handicap = db.relationship('Handicap', secondary="admin_user_handicap", backref=db.backref('user'), lazy='dynamic')

    ## 添加部门组
    handicap_id = db.Column(db.Integer, db.ForeignKey('admin_handicap.id'))


    ## 添加是否超级管理员
    is_super = db.Column(db.Integer, default=0, comment='是否超级管理员')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 基于 Token 验证
    def generate_auth_token(self, secret_key, expiration=600):
        s = TimedJSONWebSignatureSerializer(
            secret_key, expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token,secret_key):
        '''Token 验证'''
        # 判断 Token 是否在 Redis 数据库中，如果不在，则返回
        # is_blacklisted_token = BlacklistToken.check_blacklist(token)
        # if is_blacklisted_token:
        #     return None
        

        s = TimedJSONWebSignatureSerializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:  # Expiration of token
            raise AuthFailed(msg='令牌已过期')
        except BadSignature:
            raise AuthFailed(msg='无效的令牌')        # Invalid token

        # 从 Redis 数据库读取存储认证的用户
        is_exist = Redis.hget(name=current_app.config['REDIS_SAVE_TOKEN_NAME'], key=data['id'])
        if not is_exist:
            raise AuthFailed(msg='数据库中未找到令牌')

        user = User.query.get(data['id'])
        if not user:
            return AuthFailed(msg='此令牌用户无效')
        return user


# 角色表
class Role(db.Model):
    __tablename__ = 'admin_role'
    id = db.Column(db.Integer, primary_key=True, comment='角色ID')
    name = db.Column(db.String(255), comment='角色名称')
    code = db.Column(db.String(255), comment='角色标识')
    enable = db.Column(db.Integer, comment='是否启用')
    remark = db.Column(db.String(255), comment='备注')
    details = db.Column(db.String(255), comment='详情')
    sort = db.Column(db.Integer, comment='排序')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
    power = db.relationship('Power', secondary="admin_role_power", backref=db.backref('role'))


class Power(db.Model):
    __tablename__ = 'admin_power'
    id = db.Column(db.Integer, primary_key=True, comment='权限编号')
    name = db.Column(db.String(255), comment='权限名称')
    type = db.Column(db.String(1), comment='权限类型')
    code = db.Column(db.String(30), comment='权限标识')
    url = db.Column(db.String(255), comment='权限路径')
    schema_url = db.Column(db.String(255), comment='初始化路径')  # amis 页面初始化路径
    open_type = db.Column(db.String(10), comment='打开方式')
    parent_id = db.Column(db.Integer, default=0, comment='父类编号')
    # parent_id = db.Column(db.Integer, db.ForeignKey("admin_power.id"), comment='父类编号')
    # parent = db.relationship("Power") 
    # parent = db.relationship("Power",remote_side=[id]) #  自关联
    icon = db.Column(db.String(128), comment='图标')
    sort = db.Column(db.Integer, comment='排序')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
    enable = db.Column(db.Integer, comment='是否开启')




# 创建中间表
user_role = db.Table(
    "admin_user_role",  # 中间表名称
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    db.Column("user_id", db.Integer, db.ForeignKey("admin_user.id"), comment='用户编号'),  # 属性 外键
    db.Column("role_id", db.Integer, db.ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
)



# 角色权限中间表
role_power = db.Table(
    "admin_role_power",  # 中间表名称
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    db.Column("power_id", db.Integer, db.ForeignKey("admin_power.id"), comment='用户编号'),  # 属性 外键
    db.Column("role_id", db.Integer, db.ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
)



user_handicap = db.Table(
    "admin_user_handicap",
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    db.Column("user_id", db.Integer, db.ForeignKey("admin_user.id"), comment='用户编号'),  # 属性 外键
    db.Column("handicap_id", db.Integer, db.ForeignKey("admin_handicap.id"), comment='部门编号'),  # 属性 外键
)







