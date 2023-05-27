import os
from flask import Flask

from applications.extensions import init_plugs
from applications.routers import init_routers
from applications.configs import config


def create_app(config_name=None):
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), template_folder='templates')

    

    if not config_name:
        # 尝试从本地环境中读取
        config_name = os.getenv('FLASK_ENV', 'development')

    # 引入数据库配置
    app.config.from_object(config[config_name])

    # 注册各种插件
    init_plugs(app)
    # 注册路由
    init_routers(app)

    


    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        logo()

    return app


def logo():
    print('''
        ------ Welcome to China ------
    ''')
