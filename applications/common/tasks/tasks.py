# coding:utf-8
from bs4 import BeautifulSoup
import requests
from requests.packages import urllib3
# from fake_useragent import UserAgent
from random_useragent import UserAgent
import threading
from queue import Queue
from datetime import datetime
from applications.extensions import scheduler
from applications.extensions import db
from applications.models import Title,HTTPSDomain
from pyquery import PyQuery as pq
import random
# from urllib3.contrib import pyopenssl
import ssl
ssl.HAS_SNI = False


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)





tasks_list = ['check_tcp','check_ssl','check_qq','check_beian','getUrlTitle', 'getSdkTitle']




# ----------------------------------------------------- 获取域名证书剩余时间 ----------------------------------------
import re
import subprocess
from datetime import datetime


def get_re_match_result(pattern, string):
    match = re.search(pattern, string)
    return match.group(1)


def parse_time(date_str):
    return datetime.strptime(date_str, "%b %d %H:%M:%S %Y GMT")


def format_time(date_time):
    return datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S")


def get_cert_info(domain):
    """获取证书信息"""
    cmd = f"curl -Ivs https://{domain} --connect-timeout 10"

    exitcode, output = subprocess.getstatusoutput(cmd)

    # 正则匹配
    start_date = get_re_match_result('start date: (.*)', output)
    expire_date = get_re_match_result('expire date: (.*)', output)

    # 解析匹配结果
    start_date = parse_time(start_date)
    expire_date = parse_time(expire_date)

    return {
        'start_date': start_date,
        'expire_date': expire_date
    }


def get_cert_expire_date(domain):
    """获取证书剩余时间"""
    info = get_cert_info(domain)

    expire_date = info['expire_date']

    # 剩余天数
    return (expire_date - datetime.now()).days


# ---------------------------------------------------------------------------------------------


def check_tcp(*args, **kwargs):
    print("tcp")


def check_ssl(*args, **kwargs):
    with scheduler.app.app_context():
        domains_list = HTTPSDomain.query.filter_by(enable=1).all()

        result_list = []

        for url in (domains_list):
            try:
                expir_day = get_cert_expire_date(url.name)
                result_list.append({'id': url.id, 'expir_day': expir_day})
            except Exception as e:
                result_list.append({'id': url.id, 'expir_day': -1, 'remark': str(e)})

        try:
            db.session.bulk_update_mappings(HTTPSDomain, result_list)
            db.session.commit()
        except Exception as e:
            import logging
            logging.debug(str(e))


def check_qq(*args, **kwargs):
    print("qq_check")


def check_beian(*args, **kwargs):
    print("beian_check")




class BatchGetTitle:
    # pass

    def __init__(self, domains) -> None:
        self.domains = domains

        # 设置http请求头伪装成浏览器
        self.headers = {
            "User-Agent": UserAgent().android(),
        }

        self.jobs = Queue()

        self.result = []

        self.proxies_list = [
            "http://proxy.xoxoxoxo.top:18828",
            "http://proxy.xoxoxoxo.top:18829",
            "http://proxy.xoxoxoxo.top:28828",
            "http://proxy.xoxoxoxo.top:28829",
            "http://proxy.xoxoxoxo.top:28830",
            "http://proxy.xoxoxoxo.top:48828",
            "http://proxy.xoxoxoxo.top:48829",
            "http://proxy.xoxoxoxo.top:58828",
            "http://proxy.xoxoxoxo.top:58829",
        ]

    def seo_sdk_china(self, q):
        pass
        while not q.empty():
            URL  = q.get()
            try:
                proxy_ip         = random.choice(self.proxies_list)
                proxies          = { 'http': proxy_ip, 'https': proxy_ip }
                r = requests.get(url='https://seo.chinaz.com/' + URL['url'], headers=self.headers, proxies=proxies,timeout=3,verify=False)
                # r = requests.get(url='https://seo.chinaz.com/' + URL['url'], headers=self.headers, timeout=3,verify=False)
                if r.status_code < 400:
                    content          = pq(r.text) # 和requests方法一样
                    site_title       = content('#site_title').html().replace('\r\n','').replace(' ','')
                    site_keywords    = content('#site_keywords').html().replace('\r\n','').replace(' ','')
                    site_description = content('#site_description').html().replace('\r\n','').replace(' ','')
                    
                    self.result.append({'id': URL['id'],'url': URL['url'],'tag':'获取站长数据成功','status': 1,'title':site_title[:6000], 'keywords': site_keywords[:6000], 'description': site_description[:6000]})
                else:
                    self.result.append({'id': URL['id'],'url': URL['url'],'tag':'打开站长地址失败','status': 1,'title': '','keywords':'', 'description': ''})
            except Exception as e:
                self.result.append({'id': URL['id'],'url': URL['url'],'tag':'获取站长数据失败','status': 1,'title': '','keywords':'', 'description': ''})
            finally:
                q.task_done()


    def get_url_title(self,q):
        pass
        while not q.empty():
            url  = q.get()
            try:
                r = requests.get("http://"+url['url'], headers=self.headers,timeout=3, verify=False)
                status = r.status_code
                if status >= 400:
                    self.result.append({'id': url['id'],'url': url['url'],'tag':'待站长二次查询','status': 4,'title': '','keywords':'', 'description': f'{status}'})
                else:
                    if r.apparent_encoding.lower() == 'gbk':
                    # r.encoding = encoding
                        r.encoding = ('gb18030')
                    else:
                        r.encoding =  r.apparent_encoding # 解决转换乱码
                    req = pq(r.text)
                    site_title = req('title').text() or req('Title').text()
                    site_keywords = req('[name=keywords]').attr('content') or req('[name=Keywords]').attr('content')
                    site_description = req('[name=description]').attr('content') or req('[name=Description]').attr('content')
                    if site_title and site_keywords and site_description:
                        self.result.append({'id': url['id'],'url': url['url'],'tag':'获取域名页面数据成功','status': 1,'title':site_title[:6000], 'keywords': site_keywords[:6000], 'description': site_description[:6000]})
                    self.result.append({'id': url['id'],'url': url['url'],'tag':'待站长二次查询','status': 4,'title': '','keywords':'', 'description': f'{str(e)}'})
            except Exception as e:
                self.result.append({'id': url['id'],'url': url['url'],'tag':'待站长二次查询','status': 4,'title': '','keywords':'', 'description': f'{str(e)}'})
            finally:
                q.task_done()
        
        
    def sdk_runnings(self):
        run_list = []
        for url in self.domains:
            run_list.append({'id': url['id'],'url': url['url'],'tag':'准备抓取站长数据','status': 2,'title': '','keywords':'', 'description': ''})
        db.session.bulk_update_mappings(Title, run_list)
        db.session.commit()

    def url_runnings(self):
        run_list = []
        for url in self.domains:
            run_list.append({'id': url['id'],'url': url['url'],'tag':'准备抓取域名页面','status': 3,'title': '','keywords':'', 'description': ''})
        db.session.bulk_update_mappings(Title, run_list)
        db.session.commit()


    def sdk_main(self):
        self.sdk_runnings()
        # 添加任务到队列中
        for domain in self.domains:
            self.jobs.put(domain)


        import multiprocessing
        workers = multiprocessing.cpu_count() * 2 + 1

        # 随机任务线程数量
        for i in range(workers):
            # worker = threading.Thread(target=self.getTitle, args=(self.jobs,))
            worker = threading.Thread(target=self.seo_sdk_china, args=(self.jobs,))
            worker.start()

        # print("waiting for queue to complete", jobs.qsize(), "tasks")
        self.jobs.join()
        # print("all done")
        return self.result
    
    def url_main(self):
        self.url_runnings()
        # 添加任务到队列中
        for domain in self.domains:
            self.jobs.put(domain)


        import multiprocessing
        workers = multiprocessing.cpu_count() * 2 + 1

        # 随机任务线程数量
        for i in range(workers):
            # worker = threading.Thread(target=self.getTitle, args=(self.jobs,))
            worker = threading.Thread(target=self.get_url_title, args=(self.jobs,))
            worker.start()

        # print("waiting for queue to complete", jobs.qsize(), "tasks")
        self.jobs.join()
        # print("all done")
        return self.result

# 0 未查询
# 1 已查询 ---> 站长查询
# 2 待查询 ---> 




def getUrlTitle(val=None):
    with scheduler.app.app_context():
        # if val is None:
        #     # val = Title.query.filter_by(status=int).all()
        #     val = list(map(lambda o:{'id': o.id,'url': o.url}, Title.query.filter_by(status=int).all()[:500]))
        # if len(val) > 0:

        # n = 0
        # while 0 > -1:
        if val is None:
            # 先判断是否有正在查询的数据,如果有数据，则跳过，
            # run_task = Title.query.filter_by(status=3).all()
            # if len(run_task) > 0:
            #     break
            # else:
            t = Title.query.filter_by(status=0).all()
            if len(t) <= 0:
                val = []
            elif len(t) > 200:
                val = list(map(lambda o:{'id': o.id,'url': o.url}, t[:200]))
            else:
                val = list(map(lambda o:{'id': o.id,'url': o.url}, t))
        else:
            list[str(val)]
        ob = BatchGetTitle(val)
        r = ob.url_main()
        try:
            db.session.bulk_update_mappings(Title, r)
            db.session.commit()
        except:
            pass
        #     db.session.rollback()
        # finally:
        #     break

def getSdkTitle(val=None):
    with scheduler.app.app_context():
        # n = 0
        # while 0 > -1:
        if val is None:
            # 先判断是否有正在查询的数据,如果有数据，则跳过，
            # run_task = Title.query.filter_by(status=2).all()
            # if len(run_task) > 0:
            #     break
            # else:
            val = list(map(lambda o:{'id': o.id,'url': o.url}, Title.query.filter_by(status=4).all()[:200]))
        else:
            list[str(val)]

        ob = BatchGetTitle(val)
        r = ob.sdk_main()
        try:
            db.session.bulk_update_mappings(Title, r)
            db.session.commit()
        except:
            db.session.rollback()
            pass
        # finally:
        #     break

# get_title([{'id': 1, 'url': 'qq.com'}])

# def get_result(val):
#     n = 0
#     while n >-1:
#         d = val[n:n+50]
#         if not d:
#             break
#         ob = BatchGetTitle(d)
#         r = ob.main()
#         print(r)
#         n = n+50

# obj = [
#         "701.com",
#         "9966.com",
#         "66612a.com",
#         "98.net",
#         "amjs.com",
#         "qq.com",
#     ]

# print(get_result(obj))