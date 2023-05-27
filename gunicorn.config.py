import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
bind = "0.0.0.0:8000"
timeout = 60

# threads = 2

# 日志相关
# import os
# chdir = os.path.dirname(os.path.abspath(__file__))
# loglevel = 'info'
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 
# if not os.path.exists('logs'):
#     os.mkdir('logs')
#     
# accesslog = os.path.join(chdir, "logs/gunicorn_access.log")
# errorlog = os.path.join(chdir, "logs/gunicorn_error.log")



# gunicorn -c gunicorn.config.py app:app
