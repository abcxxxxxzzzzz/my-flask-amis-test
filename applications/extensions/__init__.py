from flask import Flask
from .init_sqlalchemy import db, ma, init_databases
from .init_login import init_login_manager
from .init_error_views import init_error_views
from .init_mail import init_mail
from .init_upload import init_upload
from .init_dotenv import init_dotenv
from .init_redis import init_redis, Redis
from .init_apscheduler import init_scheduler,scheduler


def init_plugs(app: Flask) -> None:
    # init_login_manager(app)
    # init_dotenv()
    init_databases(app)
    init_error_views(app)
    init_mail(app)
    init_upload(app)
    init_redis(app)
    
    
    

    with app.app_context(): 
        # pass
        init_scheduler(app)