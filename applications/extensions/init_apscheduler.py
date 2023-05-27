from flask import Flask
from flask_apscheduler import APScheduler
import  fcntl, atexit
from applications.extensions import Redis

scheduler = APScheduler()


def register_memory_scheduler(app):
    """
    Flask-Apscheduler 多进程环境重复运行定时任务（解决）
        通过全局锁，控制scheduler只运行一次
        首次创建进程时，会创建一个scheduler.lock文件，并加上非阻塞互斥锁，
        此时scheduler可以成功开启，如果文件加锁失败抛出异常，则表示当前scheduler已经开启了，
        最后再注册一个退出事件，此时flask退出的话，就释放文件锁
    """
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler.init_app(app)
        scheduler.start()
    except:
        pass
 
    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
 
    atexit.register(unlock)


def register_redis_scheduler(app):
    key = f"APS_Lock"
    Redis.write(key=key, value=1, expire=180)   # 180s之后锁自动消失，因此无需释放锁。
    lock = Redis.read(key=key)                  # 第一个取出 key 的进程或者线程运行
    if lock:
        scheduler.start()
    else:
        pass

    def unlock():
        Redis.delete(key)

    atexit.register(unlock)

def init_scheduler(app: Flask) -> None:

    # 内存方式
    # register_memory_scheduler(app)

    scheduler.init_app(app)
    # with app.app_context():    
    #from applications.common.tasks import tasks
        # from applications.common.tasks import events
    register_redis_scheduler(app)
        