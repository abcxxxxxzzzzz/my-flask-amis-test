# flask配置,  1 on | 0 off, development || production
FLASK_APP      = 'app.py'
#FLASK_ENV      = 'development'
FLASK_ENV      = 'production'
FLASK_DEBUG    =  0
FLASK_RUN_HOST = '0.0.0.0'
FLASK_RUN_PORT = 5000

# pear admin flask配置
SYSTEM_NAME     = 'Flask Admin'

# MySql配置信息
# MYSQL_HOST      = '127.0.0.1'
MYSQL_HOST      = 'mysql'
MYSQL_PORT      = 3306
MYSQL_DATABASE  = 'flask'
MYSQL_USERNAME  = 'flask'
MYSQL_PASSWORD  = 'flask'

# Redis 配置
# REDIS_HOST      = '127.0.0.1'
REDIS_HOST      = 'redis'
REDIS_PORT      = 6379
REDIS_PASSWORD  = ''
REDIS_DB        = 0
REDIS_EXPIRE    = 0
REDIS_SAVE_TOKEN_NAME = 'token'   # Redis 保存 token 相关信息 redis name 值

# 密钥配置(记得改)
HEADER_TOKEN_NAME = 'X-Token'    # 传参头部 KEY 值
SECRET_KEY='pear-admin-flask'    # 加密秘钥
SECRET_EXPIRATION = 86400        # Token有效期


# 邮箱配置
MAIL_SERVER='smtp.qq.com'
MAIL_USERNAME='123@qq.com'
MAIL_PASSWORD='XXXXX' # 生成的授权码