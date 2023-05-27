import logging
import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

# -------------- 读取 .env 变量 ---------------------
from dotenv import load_dotenv
root_path = os.path.abspath(os.path.dirname(__file__)).split('applications')[0]
# dot_env_path = os.path.join(root_path, '.env')
flask_env_path = os.path.join(root_path, '.flaskenv')
if os.path.exists(flask_env_path):
    load_dotenv(flask_env_path)
# --------------------------------------------------
 
class BaseConfig:

    SYSTEM_NAME = os.getenv('SYSTEM_NAME', 'Flask Admin')

    UPLOADED_PHOTOS_DEST = 'static/upload'
    UPLOADED_FILES_ALLOW = ['gif', 'jpg']
    UPLOADS_AUTOSERVE = True

    # JSON配置
    JSON_AS_ASCII = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    SECRET_EXPIRATION = int(os.getenv('SECRET_EXPIRATION', 86400))
    HEADER_TOKEN_NAME = os.getenv('HEADER_TOKEN_NAME', 'X-Token')
    

    # Redis配置
    REDIS_HOST = os.getenv('REDIS_HOST') or "127.0.0.1"
    REDIS_PORT = int(os.getenv('REDIS_PORT') or 6379)
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD') or ''
    REDIS_DB = int(os.getenv('REDIS_DB') or 0)
    REDIS_EXPIRE = int(os.getenv('REDIS_EXPIRE') or 0)
    REDIS_SAVE_TOKEN_NAME = os.getenv('REDIS_SAVE_TOKEN_NAME') or ''

    
    # 默认日志等级配置
    LOG_LEVEL = logging.WARN

    # 邮件配置
    MAIL_SERVER = os.getenv('MAIL_SERVER') or 'smtp.qq.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') or '123@qq.com'
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') or 'XXXXX'  # 生成的授权码
    # 默认发件人的邮箱,这里填写和MAIL_USERNAME一致即可
    MAIL_DEFAULT_SENDER = ('pear admin', os.getenv('MAIL_USERNAME') or '123@qq.com')


    # '''Flask-APScheduler'''
    SCHEDULER_API_ENABLED = True           # 开启API调度开关开启功能
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'   # 设置时区
    SCHEDULER_JOBSTORES = {                # 持久化配置
            'default': RedisJobStore(host=f'{REDIS_HOST}', port=f'{REDIS_PORT}',password=f'{REDIS_PASSWORD}', db=f'{REDIS_DB}')
            # 'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI),  # mysql 获取 sqlite3
            # 'default': 'mongo': MongoDBJobStore(host="127.0.0.1",port=27017, database="apscheduler", collection="jobs")
        }
    SCHEDULER_EXECUTORS = {            
        # 'default': {'type': 'threadpool', 'max_workers': 100}, # 设置定时任务的执行器（默认是最大执行数量为10的线程池）
        'default': ThreadPoolExecutor(100),    # 线程池配置，最大20个线程
        'processpool': ProcessPoolExecutor(10)
    }
    SCHEDULER_JOB_DEFAULTS = {'misfire_grace_time':300}       # 设置容错时间为 1小时
    # SCHEDULER_API_PREFIX = '/scheduler' # API 前缀
    # SCHEDULER_ALLOWED_HOSTS = ['*']     # 允许执行定时任务的主机名
    # SCHEDULER_AUTH = HTTPBasicAuth()    # auth验证。默认是关闭的，


# class TestingConfig(BaseConfig):
#     """ 测试配置 """
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     SQLALCHEMY_ECHO = False


class DevelopmentConfig(BaseConfig):
    """ 开发配置 """
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_ECHO = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False



class ProductionConfig(BaseConfig):
    """生成环境配置"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_RECYCLE = 8

    # mysql 配置
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME') or "root"
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD') or "123456"
    MYSQL_HOST = os.getenv('MYSQL_HOST') or "127.0.0.1"
    MYSQL_PORT = int(os.getenv('MYSQL_PORT') or 3306)
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE') or "FlaskAdmin"

    # mysql 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"



    LOG_LEVEL = logging.ERROR
    



config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    'production': ProductionConfig
}
