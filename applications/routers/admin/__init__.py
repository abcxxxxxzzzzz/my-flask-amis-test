from flask import Flask
from .auth import auth_bp
from .index import index_bp
from .user import admin_user
from .role import admin_role
from .power import admin_power
from .photo import admin_photo
from .log import admin_log
from .task import admin_task
from .monitor import admin_monitor

from .live.handicap import admin_handicap
from .live.member import admin_member
from .live.tag import admin_tag

from .other.title import admin_title
from .other.https import admin_domain_https

def register_admin_views(app: Flask):
    app.register_blueprint(auth_bp,        url_prefix='/admin')
    app.register_blueprint(index_bp,       url_prefix='/admin')
    app.register_blueprint(admin_user,     url_prefix='/admin')
    app.register_blueprint(admin_role,     url_prefix='/admin')
    app.register_blueprint(admin_power,    url_prefix='/admin')
    app.register_blueprint(admin_photo,    url_prefix='/admin')
    app.register_blueprint(admin_log,      url_prefix='/admin')
    app.register_blueprint(admin_task,     url_prefix='/admin')
    app.register_blueprint(admin_monitor,  url_prefix='/admin')

    app.register_blueprint(admin_handicap, url_prefix='/admin')
    app.register_blueprint(admin_member,   url_prefix='/admin')
    app.register_blueprint(admin_tag,      url_prefix='/admin')

    app.register_blueprint(admin_title,        url_prefix='/admin')
    app.register_blueprint(admin_domain_https, url_prefix='/admin')

# from applications.view.admin.admin_log import admin_log
# from applications.view.admin.dict import admin_dict
# from applications.view.admin.index import admin_bp
# from applications.view.admin.file import admin_file
# from applications.view.admin.power import admin_power
# from applications.view.admin.role import admin_role
# from applications.view.admin.user import admin_user
# from applications.view.admin.monitor import admin_monitor_bp
# from applications.view.admin.task import admin_task


# def register_admin_views(app: Flask):
#     app.register_blueprint(admin_bp)
#     app.register_blueprint(admin_user)
#     app.register_blueprint(admin_file)
#     app.register_blueprint(admin_monitor_bp)
#     app.register_blueprint(admin_log)
#     app.register_blueprint(admin_power)
#     app.register_blueprint(admin_role)
#     app.register_blueprint(admin_dict)
#     app.register_blueprint(admin_task)
