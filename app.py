from applications import create_app
from flask_migrate import Migrate
from applications.extensions import db



app = create_app()

migrate = Migrate(app, db)


# 创建超级管理员
import click
from applications.models.admin_rbac import User
@app.cli.command('createsuperadmin')
@click.option('--username', default='admin')
def create_user(username):
    obj = User()
    obj.username = username
    obj.realname = username
    obj.enable = 1
    obj.set_password(username)
    db.session.add(obj)
    db.session.commit()
    
    
    

    click.echo(f'Create: {username}!')
    click.echo(f'Passwd: {username}!')

if __name__ == '__main__':
    app.run()



# from flask import Flask, render_template,json,jsonify
# from .jsonp import menu,main,main_list

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')


# # 渲染菜单
# @app.route('/menu')
# def get_menu():
#     res = {"status": 0,"msg": "", "data": menu }
#     return jsonify(res)

# # 渲染内容
# @app.route("/main")
# def get_main():
#     res = {"status": 0,"msg": "", "data": main }
#     return jsonify(res)


# @app.route("/main/list")
# def get_main_list():
#     res = {"status": 0,"msg": "", "data": main_list }
#     return jsonify(res)



# if __name__ == "main":
#     app.run()





# export FLASK_ENV=development
# export FLASK_APP=app.py