import tornado.web
import time
import math
import bisect
from tornado.escape import json_encode
from comm import elasapi
from comm  import auth
from comm import comm
#导入数据库
from comm import database

#--计算时间
import time
import functools

def outer(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        start_time = time.time()
        res = func(self, *args, **kwargs)
        end_time = time.time()
        if isinstance(res, dict):
            res["time"] = '{:.2f}'.format(end_time - start_time)
        print(end_time - start_time)
        return res
    return inner


class LoginHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render("login.html")

    def post(self, *args, **kwargs):
        username = self.get_argument('form-username')
        passwd   = self.get_argument('form-password')
        auth_user = auth.check_user(username,passwd)
        if auth_user:
            self.set_secure_cookie("username",username,httponly=True,expires_days=1)
            self.redirect("/")
        else:
            self.redirect("/login")

class LogoutHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie("username")
        self.redirect("/")

class MainHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("username")
        return user

class IndexHandler(MainHandler):
    @tornado.web.authenticated
    def get(self):
        username = tornado.escape.xhtml_escape(self.current_user)
        self.render("index.html", user=username)

#汇总公司的人员的拜访次数统计
class GroupByCompanyHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("gpost.html")

    def valueMap(self,res):
        res = res["by_user"]["buckets"]
        all_keys = ["0", "1", "2"]
        if len(res) < 3:
            key = [ k["key"] for k in res ]
            no_keys = list( set(all_keys) - set(key) )
            res.extend([ {'doc_count': 0, 'unique': {'value': 0}, 'key': str(_) } for _ in no_keys ])
            res.sort(key=lambda s: s["key"])
        return res

    def post(self, *args, **kwargs):
        start_date = self.get_argument("start_date")
        end_date = self.get_argument("end_date")
        res_size = self.get_argument("size") or 10
        company  = self.get_argument("company", None)
        if not end_date and not start_date:
            #未指定日期
            pass
        if company:
            company_sql = '''
                           select a.corp_id,a.unitname from pub_corp a where a.unitname in :1
                         '''
            db = database.Connection()
            company =  db.get(company_sql,company)["CORP_ID"]
        starttime = time.time()
        '''此处查找总的拜访次数
        res = elasapi.group_by_company("test-index",
                                   start_date=start_date,
                                   end_date=end_date,
                                   size=100)
        '''
        res = elasapi.search_by_cust_id("test-index",
                                        start_date=start_date,
                                        end_date=end_date,
                                        size=res_size,company=company)
        endtime = time.time()
        res["time"] = "{:.2f}".format(endtime - starttime)
        #修改汇总数据中的 "-" 为 0
        list(map(self.valueMap, res["buckets"]))

        self.set_header("Content-Type","application/json;charset=UTF-8")
        self.finish(res)

class AnalyzeByCompanyVisitHandler(tornado.web.RequestHandler):
    '''
        根据公司分每个人的拜访次数
        或      每个人的拜访次数
    '''
    def get(self, *args, **kwargs):
        starttime = time.time()
        res = elasapi.group_by_company("test-index",
                                   start_date="2017/02/12",
                                   end_date='2017/02/13',
                                   size=100)
        endtime = time.time()
        print(endtime - starttime)
        MaxVisitCount = res["buckets"][0]["doc_count"]
        groups = math.ceil(int(MaxVisitCount) / 10)
        x_series= [ x  for x in range(MaxVisitCount) if x % groups == 0 ]
        y=[ bisect.bisect(x_series,(i["doc_count"]) ) for i in res["buckets"] ]
        y.reverse()
        y_series = [ y.count(e_y) for e_y in set(y) ]
        res["x_series"] = x_series
        res["y_series"] = y_series
        print(res)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.finish(json_encode(res))

class GroupByEmployeeHandler(tornado.web.RequestHandler):
    '''
        返回根据拜访时间排序的数据
    '''
    def get(self):
        res = elasapi.group_by_employee("test-index",
                                        start_date="2017/02/01",
                                        end_date="2017/02/01",
                                        interval=True,
                                        size=5)
        self.render("user.html", data=res)
        #self.finish(res)

class EchartsHandler(tornado.web.RequestHandler):
    def get(self, echart):
        self.render("%s.html" % echart)

class TestHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render("index1.html")

class AnalyzeByPersonVisitHandler(tornado.web.RequestHandler):

    def get(self,*args,**kwargs):
        res = elasapi.test("test-index", size=10, start_date="2017/02/11 00:00",
               end_date="2017/02/11 11:00", doc_type="mb_report")
        buckets = [ _["_source"]for _ in res["hits"]["hits"]]
        res = res["aggregations"]["by_day"]["buckets"]
        d = {}
        d["x_series"] = [ _["key_as_string"] for _ in res ]
        d["y_series"] = [ _["doc_count"] for _ in res ]
        d["buckets"] = buckets
        self.set_header("Access-Control-Allow-Origin", "*")
        self.finish(json_encode(d))

#公司当月每天的拜访次数的趋势图
class ApiCompanyTrendHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("companytrend.html")

    def post(self, *args, **kwargs):
        month = self.get_argument("month")
        company = self.get_argument("q")
        start_date, end_date = comm.getMonthFirstDayAndLastDay(month=month)
        res = elasapi.search_key("test-index",start_date=start_date,
                                   end_date=end_date,key="PK_CORP")
        data = {}
        x_series = []
        y_series =[]
        for d in res:
            x_series.append(d["key_as_string"])  #日期
            y_series.append(d["doc_count"])      #次数
        data["x_series"] = list(map(lambda x: x.split()[0] , x_series))
        data["y_series"] = y_series
        self.set_header("Content-Type","application/json;charset=UTF-8")
        self.finish(data)

#个人当月每天的拜访次数的趋势图
class ApiPersonTrendHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        #start_date = self.get_argument("start_date")
        #end_date = self.get_argument("end_date")
        #res_size = self.get_argument("size",10)
        month  = self.get_argument("month")
        person = self.get_argument("q")
        start_date,end_date = comm.getMonthFirstDayAndLastDay(month=month)
        res = elasapi.search_key("test-index", start_date=start_date,
                                 end_date=end_date, key="PK_USER",
                                 person_name=person)
        data = {}
        x_series = []
        y_series =[]
        for d in res:
            x_series.append(d["key_as_string"])  #日期
            y_series.append(d["doc_count"])      #次数
        data["x_series"] = list(map(lambda x: x.split()[0] , x_series))
        data["y_series"] = y_series
        self.set_header("Content-Type","application/json;charset=UTF-8")
        self.finish(data)

#查询个人月拜时，自动补全查询对话框
class ApiAutoCompleteHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("t1.html")
    def post(self):
        l = ["218CEA10-237F-11E5-AA10-F3DFF09504A9","26F79860-1A85-11E3-9860-D2A88FA7BD89"]
        data =json_encode(l)
        self.finish(data)

class NginxConfigHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("company.html")