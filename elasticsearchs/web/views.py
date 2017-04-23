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
import datetime
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
        company  = self.get_argument("q", None)
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
        res = elasapi.search_by_cust_id("test-index",
                                        start_date=start_date,
                                        end_date=end_date,
                                        size=10,company=company)
        endtime = time.time()
        res["time"] = "{:.2f}".format(endtime - starttime)
        #修改汇总数据中的 "-" 为 0
        list(map(self.valueMap, res["buckets"]))
        self.set_header("Content-Type","application/json;charset=UTF-8")
        self.finish(res)

class EchartsHandler(tornado.web.RequestHandler):
    def get(self, echart):
        self.render("%s.html" % echart)

#公司日拜访次数
class AnalyzeByCompanyVisitHandler(tornado.web.RequestHandler):
    def listtogroup(self,lreq):
        res = []
        for i in enumerate(lreq):
            try:
                test = "[" + str(i[1]) + "," + str(lreq[i[0] + 1]) + ")"
            except:
                test = "[" + str(i[1]) + "," + ")"
            res.append(test)
        return res
    def post(self, *args, **kwargs):
        company = self.get_argument("q", None)
        if company:
            company_sql = '''
                  select a.corp_id,a.unitname from pub_corp a where a.unitname in :1
                                 '''
            db = database.Connection()
            company = db.get(company_sql, company)["CORP_ID"]
        starttime = time.time()
        res = elasapi.search_by_date("test-index",
                                   start_date="2017/02/12",
                                   end_date='2017/02/13',
                                   company_name = company)
        endtime = time.time()
        MaxVisitCount = res["buckets"][0]["doc_count"]
        groups = math.ceil(int(MaxVisitCount) / 10)
        x_series = [x for x in range(MaxVisitCount) if x % groups == 0]
        '''
            请不要装逼,  ( ^_^ ) 没有改变就没有伤害 ( ^_^ )
            x_series = [0, 9, 18, 27, 36, 45, 54, 63, 72, 81]
            y = [1]*10 + [10]*2 + [53]*2
            x_series = ['[0,9)','[9,18)'...,'[63,72)', '[72,81)', '[81,)']
            y_series = [(1,10),(2,2),(3,0),(4,0),(5,0),(6,2)...(10,0)]
            result = xxoo
        '''
        # ---------------格式化数据----开始
        y = [bisect.bisect(x_series, (i["doc_count"])) for i in res["buckets"]]
        y.reverse()
        y = [(_, y.count(_)) for _ in set(y)]
        y.extend( list(map(lambda x: (x, 0),list(
                set( [ _[0] for _ in list(enumerate(x_series))[1:] ]) - set([_[0] for _ in y])))) )
        y.sort(key=lambda x: x[0])
        y_series = [_[1] for _ in y]
        x_series = self.listtogroup(x_series)
        # ----------------格式化数据----结束
        res["x_series"] = x_series
        res["y_series"] = y_series
        self.set_header("Access-Control-Allow-Origin", "*")
        self.finish(json_encode(res))

#个人日拜分析
class AnalyzeByPersonVisitHandler(tornado.web.RequestHandler):
    corp_name = {}  #当前缓存
    def plus_half_time(sefl, strtime):
        dtime = datetime.datetime.strptime(strtime, "%H:%M:%S") + datetime.timedelta(minutes=30)
        res = time.strftime('%H:%M:%S', dtime.timetuple())
        return res

    def convert_corp_name(self,cname):
        if not self.corp_name.get(cname["PK_CORP"],None):
            company = elasapi.person_to_company('%s' % cname["PK_CORP"])
            self.corp_name[ cname["PK_CORP"] ] = company
        cname["PK_CORP"] = self.corp_name.get(cname["PK_CORP"],'未知')
        return cname


    def post(self,*args,**kwargs):
        person = self.get_argument("q")
        start_time = time.time()
        res = elasapi.test("test-index", size=10, start_date="2017/02/12 00:00",
                                end_date="2017/02/12 11:00",
                            doc_type="mb_report")
        buckets = [ _["_source"]for _ in res["hits"]["hits"]]

        res = res["aggregations"]["by_day"]["buckets"]
        d = {}
        x_series = [ _["key_as_string"] for _ in res ]
        d["x_series"] = list( map(self.plus_half_time,list( map(lambda x: x.split()[-1], x_series ) )))
        d["y_series"] = [ _["doc_count"] for _ in res ]

        res = list(map(self.convert_corp_name, buckets))
        d["buckets"] = buckets
        end_time = time.time()
        print(end_time - start_time )
        self.set_header("Access-Control-Allow-Origin", "*")
        self.finish(json_encode(d))

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

class TestHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render("index1.html")

#公司当月每天的拜访次数的趋势图
class ApiCompanyTrendHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("companytrend.html")

    def post(self, *args, **kwargs):
        month = self.get_argument("month")
        company = self.get_argument("q",None)
        if company:
            company_sql = '''
                      select a.corp_id,a.unitname from pub_corp a where a.unitname in :1
                                 '''
            db = database.Connection()
            company = db.get(company_sql, company)["CORP_ID"]

        start_date, end_date = comm.getMonthFirstDayAndLastDay(month=month)
        res = elasapi.search_key("test-index",start_date=start_date,
                                   end_date=end_date,key="PK_CORP",
                                 company_name=company)
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
        word = self.get_argument("query", None)
        q_type = self.get_argument("q_type", None)  #LoadCompanyTrend,LoadPersonTrend
        # sql = '''
        #       select a.corp_id,a.unitname from pub_corp a where a.unitname like :1
        #       '''
        #
        # t = database.Connection()
        # ss = t.query(sql, word + "%")
        # print(ss)
        # l = [ i['UNITNAME'] for i in ss ][:10]
        if q_type is None or q_type == "LoadCompanyTrend" or q_type == "LoadCompanyColumnGraph":
            res = elasapi.query_word(word)
            l = [_["_source"]["UNITNAME"] for _ in res["hits"]["hits"]]
        else:
            res = elasapi.query_word(word,key="PSNNAME",doc_type="person")
            l = [ _["_source"]["PSNNAME"] for _ in res["hits"]["hits"] ]
            print(res)
        data =json_encode(l)
        self.finish(data)

class NginxConfigHandler(tornado.web.RequestHandler):
    pass

#统计数据中的个人明细数据
class LoadPersonOnGpost(tornado.web.RequestHandler):
    #
    def valueMap(self, res):
        if res["by_user"]["buckets"] == []:
            res["by_user"]["buckets"] = [{"by_user": {"buckets":[]}}]
        res = res["by_user"]["buckets"][0]["by_user"]["buckets"]
        all_keys = ["0", "1", "2"]
        if len(res) < 3:
            key = [k["key"] for k in res]
            no_keys = list(set(all_keys) - set(key))
            res.extend([{'doc_count': 0,  'key': str(_)} for _ in no_keys])
            res.sort(key=lambda s: s["key"])
        return res

    def post(self, *args, **kwargs):
        company_name = self.get_argument('company', None)
        start_date= self.get_argument('start_date')
        end_date  = self.get_argument('end_date')
        person    = self.get_argument("person_name")
        res = elasapi.search_key("test-index", start_date=start_date,
                                  end_date=end_date, key="PK_USER",
                                 person_name=person,multi_trend=True)

        list(map(self.valueMap, res))
        data = {}
        x_series = []
        y_series =[]
        y_0 = []
        y_1 = []
        y_2 = []

        for d in res:
            print(d)
            x_series.append(d["key_as_string"])  #日期
            y_series.append(d["doc_count"])      #次数
            for i in d["by_user"]["buckets"][0]["by_user"]["buckets"]:
                if i["key"] == '0': y_1.append('%s' % i["doc_count"])
                if i["key"] == '1': y_0.append(str(i["doc_count"]))
                if i["key"] == '2': y_2.append(str(i["doc_count"]))


        data["x_series"] = list(map(lambda x: x.split()[0] , x_series))
        data["x_series"] = x_series
        data["y_series"] = y_series
        data['y_0'] = y_0
        data['y_1'] = y_1
        data['y_2'] = y_2
        self.set_header("Content-Type","application/json;charset=UTF-8")
        self.finish(data)