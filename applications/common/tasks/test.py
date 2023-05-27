# coding:utf-8
from bs4 import BeautifulSoup
import requests
from requests.packages import urllib3
from fake_useragent import UserAgent
import threading
from queue import Queue




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




class BatchGetTitle:

    def __init__(self, domains) -> None:
        self.domains = domains

        # 设置http请求头伪装成浏览器
        self.headers = {
            "User-Agent": UserAgent().random,
        }

        self.jobs = Queue()

        self.result = []

        
        # requests获取博客页面html文本



    def getTitle(self,q):

        while not q.empty():
            url  = q.get()
            try:
                r = requests.get("http://"+url, headers=self.headers,timeout=3, verify=False)
                status = r.status_code
                if status >= 400:
                    self.result.append({'url': url,'tag':'访问错误','title': ''})
                else:
                    # r.encoding = encoding
                    r.encoding =  r.apparent_encoding # 解决转换乱码
                    html = r.text
                    soup = BeautifulSoup(html, "html.parser")

                    pagetitle = soup.find("title")
                    if pagetitle is None:
                        self.result.append({'url': url,'tag':'无标题','title': ''})
                    else:
                        title = pagetitle.get_text().replace(' ', '')
                        if len(title) == 0:
                            self.result.append({'url': url,'tag':'无标题','title': ''})
                        else:
                            self.result.append({'url': url,'tag':'有标题','title':title})
            except:
                
                self.result.append({'url': url,'tag':'无法访问','title': ''})
            
            finally:
                q.task_done()

                # 插入到任务情况数据库，再清空 self.result
                # print(len(self.result))
                # print(len(self.result))

                           
                

    def main(self):
        # 添加任务到队列中
        for domain in self.domains:
            self.jobs.put(domain)


        # 随机任务线程数量
        for i in range(10):
            worker = threading.Thread(target=self.getTitle, args=(self.jobs,))
            worker.start()

        # print("waiting for queue to complete", jobs.qsize(), "tasks")
        self.jobs.join()
        # print("all done")
        return self.result


def get_result(val):
    n = 0
    while n >-1:
        d = val[n:n+50]
        if not d:
            break
        ob = BatchGetTitle(d)
        r = ob.main()
        print(r)
        n = n+50



obj = [
        "701.com",
        "9966.com",
        "66612a.com",
        "98.net",
        "amjs.com",
        "qq.com",
    ]

print(get_result(obj))