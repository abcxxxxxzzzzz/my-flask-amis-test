import json,uuid

from flask import Blueprint, render_template, request, current_app, views,g
from applications.common.utils.http import Success,UpdateSuccess,DeleteSuccess,ParameterException,NotFound
from applications.common.utils.jsoncoder import DateEncoder
from applications.extensions import scheduler
from applications.common.tasks import tasks
from applications.common.tasks.tasks import tasks_list
from flask_apscheduler.utils import job_to_dict
from applications.common.utils.rights import authenticate
from applications.jsonp.rbac.jsonp_task import getTaskJson
from applications.common.helper import ModelFilter
from applications.common.utils.validate import xss_escape
from applications.models import Title

admin_task = Blueprint('adminTask', __name__)


class TaskAllAPIViews(views.MethodView):
    def get(self):
        data = {"options": []}
        for i in tasks_list:
            data['options'].append({ "label": i, "value": i})

        return Success(data=data)

class TaskTempAPIViews(views.MethodView):

    @authenticate(power='admin:task', log=False)
    def get(self):
        data = getTaskJson(g.permissions)
        return Success(data=data)


class TaskListAPIViews(views.MethodView):
    
    @authenticate(power='admin:task:list', log=False)
    def get(self):
        jobs = scheduler.get_jobs()
        jobs_list = []
        for job in jobs:
            order_info = job_to_dict(job)
            order_info['second'] = order_info.get("second") or order_info.get("seconds") or ''
            order_info['minute'] = order_info.get("minute") or order_info.get("minute") or ''
            order_info['hour'] = order_info.get("hour") or order_info.get("hours") or ''
            order_info['enable'] = 1 if order_info['next_run_time'] else 0     # 添加自定义字段
            jobs_list.append(json.loads(json.dumps(order_info, cls=DateEncoder)))
        return Success(data={'rows': jobs_list, 'total': len(jobs_list)})


class TaskAPIViews(views.MethodView):
    
    @authenticate(power='admin:task:show', log=False)
    def get(self, id):
        job = scheduler.get_job(id)
        order_info = job_to_dict(job)
        return Success(data=json.loads(json.dumps(order_info, cls=DateEncoder)))

    @authenticate(power='admin:task:add', log=True)
    def post(self):
        req       = request.json
        id        = str(uuid.uuid1())
        name      = req.get("name")
        type      = req.get("type")
        functions = req.get("functions")
        datetime  = req.get("datetime")
        

        '''先判断需要执行的任务是否存在'''
        if not hasattr(tasks, functions):
            return ParameterException()

        ''' replace_existing 可添加重复ID的'''
        if type == 'date':                        # 一次性任务
            scheduler.add_job(
                func=getattr(tasks, functions),
                id=id,
                name=name,
                trigger=type,
                run_date=datetime,
                replace_existing=True,
                coalesce=True)   

        elif type == 'interval':                  # 间隔调度
            seconds   = int(req.get('seconds', 0))
            if seconds <= 0:
                raise ParameterException(msg='间隔任务时间不能小于0')

            scheduler.add_job(
                func=getattr(tasks, functions),
                id=id,
                name=name,
                seconds=seconds,
                trigger=type,
                replace_existing=True,
                coalesce=True)   

        elif type == 'cron':                       # 周期调度
            # print(req)
            day_of_week = req.get('day_of_week')
            hour = req.get('hour')
            minute = req.get('minute')
            seconds = req.get('second')
            scheduler.add_job(
                func=getattr(tasks, functions),
                id     = id,
                name   = name,
                second = seconds,
                minute = minute,
                hour   = hour,
                day_of_week   = day_of_week,
                trigger= type,
                replace_existing=True)   
        else:
            raise ParameterException(msg='无效的触发器')

        return Success()

    @authenticate(power='admin:task:del', log=True)
    def delete(self,id):
        try:
            scheduler.remove_job(id)
        except Exception as e:
            raise ParameterException(msg=str(e))
        return DeleteSuccess(msg="任务已删除")


class TaskSwitchAPIViews(views.MethodView):

    decorators = [authenticate("admin:task:edit", log=True)]

    
    def post(self, id):
        try:
            scheduler.run_job(id)
        except Exception as e:
            raise ParameterException(msg=str(e))
        return UpdateSuccess(msg="立即运行成功")

    
    def put(self, id):
        req = request.json
        enable = int(xss_escape(req.get('enable')))
        try:
            if enable:
                scheduler.resume_job(id) # 启动
            else:
                scheduler.pause_job(id)  # 暂停
        except Exception as e:
            raise ParameterException(msg=str(e))
        return UpdateSuccess(msg="状态已切换")

admin_task.add_url_rule('/task/all',             view_func=TaskAllAPIViews.as_view('taskAll'),      endpoint='taskAll',    methods=['GET'])     # 模板
admin_task.add_url_rule('/task/temp',            view_func=TaskTempAPIViews.as_view('taskTemp'),     endpoint='taskTemp',   methods=['GET'])     # 模板
admin_task.add_url_rule('/task/list',            view_func=TaskListAPIViews.as_view('taskList'),     endpoint='taskList',   methods=['GET'])     # 列表
admin_task.add_url_rule('/task/<id>',            view_func=TaskAPIViews.as_view('task'),             endpoint='task',       methods=['GET','PUT','DELETE'])     # 列表
admin_task.add_url_rule('/task',                 view_func=TaskAPIViews.as_view('taskAdd'),          endpoint='taskAdd',    methods=['POST'])    # 列表
admin_task.add_url_rule('/task/status/<id>',     view_func=TaskSwitchAPIViews.as_view('taskStatus'), endpoint='taskStatus', methods=['PUT'])     # 切换状态
admin_task.add_url_rule('/task/run/<id>',        view_func=TaskSwitchAPIViews.as_view('taskRun'),    endpoint='taskRun', methods=['POST'])     # 切换状态

