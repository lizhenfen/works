import tornado.web
import time
import math
import bisect
from tornado.escape import json_encode
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import tornado.web
import tornado.gen

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


class OracleQueryHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    def initialize(self):
        self.db = database.Connection()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        data = {}
        query_time = yield self.query_all()
        data["time"] = query_time
        self.write(data)
        self.finish()

    @run_on_executor
    def query_all(self,*args):
        sql = '''
                   select son.pk_corp,
               dept.deptname,
               son.psnname,
               cl.psnclname,
               '201701'yearmonth,
               sum(nvl(countscust.usercustcounts, '0')) usercustcounts,
               sum(nvl(custvisit.countcustvisit, '0')) countcustvisit,
               sum(nvl(custvisittime.contcustvisittime, '0')) contcustvisittime,
               sum(nvl(addcust.addcusts, '0')) addcusts,
               sum(nvl(addupcustvisit.addupcustvisits, '0')) addupcustvisits,
               sum(nvl(adduptime.adduptimes, '0')) adduptimes,
               sum(nvl(jxscount.jxscounts, '0')) jxscounts,
               sum(nvl(jxsvisit.countjxsvisit, '0')) countjxsvisit,
               sum(nvl(jxsvisittime.contjxsvisittime, '0')) contjxsvisittime,
               sum(nvl(addupjxsvisit.addupjxsvisits, '0')) addupjxsvisits,
               sum(nvl(addupjxstime.addupjxstimes, '0')) addupjxstimes,
               sum(nvl(tgcount.tgcounts, '0')) tgcounts,
               sum(nvl(tgvisit.counttgvisit, '0')) counttgvisit,
               sum(nvl(tgvisittime.conttgvisittime, '0')) conttgvisittime,
               sum(nvl(addtgcust.addtgcusts, '0')) addtgcusts,
               sum(nvl(adduptgvisit.adduptgvisits, '0')) adduptgvisits,
               sum(nvl(adduptgtime.adduptgtimes, '0')) adduptgtimes,
               sum(nvl(zdcount.zdcounts, '0')) zdcounts,
               sum(nvl(zdvisit.countzdvisit, '0')) countzdvisit,
               sum(nvl(zdvisittime.contzdvisittime, '0')) contzdvisittime,
               sum(nvl(addzdcust.addzdcusts, '0')) addzdcusts,
               sum(nvl(addupzdvisit.addupzdvisits, '0')) addupzdvisits,
               sum(nvl(addupzdtime.addupzdtimes, '0')) addupzdtimes,
               sum(nvl(Azdcount.Azdcounts, '0')) Azdcounts,
               sum(nvl(Azdvisit.Acountzdvisit, '0')) Acountzdvisit,
               sum(nvl(Azdvisittime.Acontzdvisittime, '0')) Acontzdvisittime,
               sum(nvl(Aaddzdcust.Aaddzdcusts, '0')) Aaddzdcusts,
               sum(nvl(Aaddupzdvisit.Aaddupzdvisits, '0')) Aaddupzdvisits,
               sum(nvl(Aaddupzdtime.Aaddupzdtimes, '0')) Aaddupzdtimes,
               sum(nvl(Bzdcount.Bzdcounts, '0')) Bzdcounts,
               sum(nvl(Bzdvisit.Bcountzdvisit, '0')) Bcountzdvisit,
               sum(nvl(Bzdvisittime.Bcontzdvisittime, '0')) Bcontzdvisittime,
               sum(nvl(Baddzdcust.Baddzdcusts, '0')) Baddzdcusts,
               sum(nvl(Baddupzdvisit.Baddupzdvisits, '0')) Baddupzdvisits,
               sum(nvl(Baddupzdtime.Baddupzdtimes, '0')) Baddupzdtimes,
               sum(nvl(Czdcount.Czdcounts, '0')) Czdcounts,
               sum(nvl(Czdvisit.Ccountzdvisit, '0')) Ccountzdvisit,
               sum(nvl(Czdvisittime.Ccontzdvisittime, '0')) Ccontzdvisittime,
               sum(nvl(Caddzdcust.Caddzdcusts, '0')) Caddzdcusts,
               sum(nvl(Caddupzdvisit.Caddupzdvisits, '0')) Caddupzdvisits,
               sum(nvl(Caddupzdtime.Caddupzdtimes, '0')) Caddupzdtimes,
               sum(nvl(ph.phcounts, '0')) phcounts,
               sum(nvl(noph.nophcounts, '0')) nophcounts,
               sum(nvl(dx.dxcounts, '0')) dxcounts,
               sum(nvl(nodx.nodxcounts, '0')) nodxcounts

          from bd_person son
          left join bd_psncl cl on son.pk_psncl = cl.pk_psncl
          left join bd_dept dept on son.pk_dept = dept.pk_dept
          left join (select sum(usercustcounts) usercustcounts, pk_user
                       from (select count(cu.pk_cust) usercustcounts, sons.pk_user
                               from bd_cust cu
                               left join bd_person sons on cu.pk_psn = sons.pk_psn
                              where nvl(cu.sealflag, 'N') = 'N'
                                and nvl(cu.dr, '0') = '0'
                              group by sons.pk_user
                             union all
                             select count(cust.pk_psnalcust) usercustcounts,
                                    son.pk_user
                               from bd_psnalcust cust
                               left join bd_person son on cust.pk_psn = son.pk_psn
                               left join bd_custcl cl on cust.pk_custcl =
                                                         cl.pk_custcl
                               left join bd_custmodel el on cl.pk_custmodel =
                                                            el.pk_custmodel
                              where nvl(cust.sealflag, 'N') = 'N'
                                and nvl(cust.dr, '0') = '0'
                                and el.modelcode in ('02', '03')
                              group by son.pk_user)
                      group by pk_user) countscust on son.pk_user =
                                                      countscust.pk_user
          left join (select pk_user, sum(countcustvisit) countcustvisit
                       from (select pk_user, count(pk_cust) countcustvisit
                               from (select hh.pk_user, hh.pk_cust
                                       from bd_cust cu
                                      right join mb_custvisit_h hh on cu.pk_cust =
                                                                      hh.pk_cust
                                      where hh.vdate >= '2017-01-01' and
                                            hh.vdate <= '2017-02-01'
                                      group by hh.pk_user, hh.pk_cust)
                              group by pk_user
                             union all
                             select pk_user, count(pk_cust) countcustvisit
                               from (select hh.pk_user, hh.pk_cust
                                       from bd_psnalcust cu
                                       left join bd_custcl cl on cu.pk_custcl =
                                                                 cl.pk_custcl
                                       left join bd_custmodel el on cl.pk_custmodel =
                                                                    el.pk_custmodel
                                       left join mb_psnalcustvisit_h hh on cu.pk_psnalcust =
                                                                           hh.pk_cust
                                      where el.modelcode in ('02', '03')
                                        and hh.pk_user is not null
                                        and hh.vdate >= '2017-01-01'
        			                	and hh.vdate <= '2017-02-01'
                                      group by hh.pk_user, hh.pk_cust)
                              group by pk_user)
                      group by pk_user) custvisit on son.pk_user =
                                                     custvisit.pk_user
          left join (select pk_user, sum(contcustvisittime) contcustvisittime
                       from (select count(hh.pk_custvisit_h) contcustvisittime,
                                    hh.pk_user
                               from bd_cust cus
                              right join mb_custvisit_h hh on cus.pk_cust =
                                                              hh.pk_cust
                              where hh.vdate >= '2017-01-01'
        		                and hh.vdate <= '2017-02-01'
                              group by hh.pk_user
                             union all
                             select count(hh.pk_custvisit_h) contcustvisittime,
                                    hh.pk_user
                               from bd_psnalcust cus
                               left join bd_custcl cl on cus.pk_custcl = cl.pk_custcl
                               left join bd_custmodel el on cl.pk_custmodel =
                                                            el.pk_custmodel
                               left join mb_psnalcustvisit_h hh on cus.pk_psnalcust =
                                                                   hh.pk_cust
                              where el.modelcode in ('02', '03')
                                and hh.pk_user is not null
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user)
                      group by pk_user) custvisittime on son.pk_user =
                                                         custvisittime.pk_user
          left join (select pk_user, sum(addcusts) addcusts
                       from (select count(cust.pk_cust) addcusts, son.pk_user
                               from bd_cust cust
                               left join bd_person son on cust.pk_psn = son.pk_psn
                              where cust.ts >= '2017-01-01'
        		        and cust.ts <= '2017-02-01'
                              group by son.pk_user
                             union all
                             select count(cust.pk_psnalcust) addcusts, son.pk_user
                               from bd_psnalcust cust
                               left join bd_person son on cust.pk_psn = son.pk_psn
                               left join bd_custcl cl on cust.pk_custcl =
                                                         cl.pk_custcl
                               left join bd_custmodel el on cl.pk_custmodel =
                                                            el.pk_custmodel
                              where el.modelcode in ('02', '03')
                                and cust.ts >= '2017-01-01'
        		            	and cust.ts <= '2017-02-01'
                              group by son.pk_user)
                      group by pk_user) addcust on son.pk_user = addcust.pk_user
          left join (select pk_user, sum(addupcustvisits) addupcustvisits
                       from (select pk_user, count(pk_cust) addupcustvisits
                               from (select hh.pk_user, hh.pk_cust
                                       from bd_cust cu
                                      right join mb_custvisit_h hh on cu.pk_cust =
                                                                      hh.pk_cust
                                      where hh.vdate <= '2017-02-01'
                                      group by hh.pk_user, hh.pk_cust)
                              group by pk_user
                             union all
                             select pk_user, count(pk_cust) addupcustvisits
                               from (select hh.pk_user, hh.pk_cust
                                       from bd_psnalcust cu
                                       left join bd_custcl cl on cu.pk_custcl =
                                                                 cl.pk_custcl
                                       left join bd_custmodel el on cl.pk_custmodel =
                                                                    el.pk_custmodel
                                       left join mb_psnalcustvisit_h hh on cu.pk_psnalcust =
                                                                           hh.pk_cust
                                      where el.modelcode in ('02', '03')
                                        and hh.pk_user is not null
                                        and hh.vdate <= '2017-02-01'
                                      group by hh.pk_user, hh.pk_cust)
                              group by pk_user)
                      group by pk_user) addupcustvisit on son.pk_user =
                                                          addupcustvisit.pk_user
          left join (select pk_user, sum(adduptimes) adduptimes
                       from (select count(hh.pk_custvisit_h) adduptimes, hh.pk_user
                               from bd_cust cus
                              right join mb_custvisit_h hh on cus.pk_cust =
                                                              hh.pk_cust
                              where hh.vdate <= '2017-02-01'
                              group by hh.pk_user
                             union all
                             select count(hh.pk_custvisit_h) adduptgtimes, hh.pk_user
                               from bd_psnalcust cus
                               left join bd_custcl cl on cus.pk_custcl = cl.pk_custcl
                               left join bd_custmodel el on cl.pk_custmodel =
                                                            el.pk_custmodel
                               left join mb_psnalcustvisit_h hh on cus.pk_psnalcust =
                                                                   hh.pk_cust
                              where el.modelcode in ('02', '03')
                                and hh.pk_user is not null
                                and hh.vdate <= '2017-02-01'
                              group by hh.pk_user)
                      group by pk_user) adduptime on son.pk_user =
                                                     adduptime.pk_user
          left join (select count(pk_cust) jxscounts, son.pk_user
                       from bd_cust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                      where cust.custprop = '0'
                        and nvl(cust.sealflag, 'N') = 'N'
                        and nvl(cust.dr, '0') = '0'
                      group by son.pk_user) jxscount on son.pk_user =
                                                        jxscount.pk_user
          left join (select pk_user, count(pk_cust) countjxsvisit
                       from (select hh.pk_user, hh.pk_cust
                               from bd_cust cu
                               left join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                              where cu.custprop = '0'
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) jxsvisit on son.pk_user = jxsvisit.pk_user
          left join (select count(hh.pk_custvisit_h) contjxsvisittime, hh.pk_user
                       from bd_cust cus
                       left join mb_custvisit_h hh on cus.pk_cust = hh.pk_cust
                      where cus.custprop = '0'
                        and hh.vdate >= '2017-01-01'
        		        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) jxsvisittime on son.pk_user =
                                                           jxsvisittime.pk_user
          left join (select pk_user, count(pk_cust) addupjxsvisits
                       from (select hh.pk_user, hh.pk_cust
                               from bd_cust cu
                              right join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                              where cu.custprop = '0'
                                and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) addupjxsvisit on son.pk_user =
                                                         addupjxsvisit.pk_user
          left join (select count(hh.pk_custvisit_h) addupjxstimes, hh.pk_user
                       from bd_cust cus
                      right join mb_custvisit_h hh on cus.pk_cust = hh.pk_cust
                      where cus.custprop = '0'
                        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) addupjxstime on son.pk_user =
                                                           addupjxstime.pk_user
          left join (select count(cust.pk_psnalcust) tgcounts, son.pk_user
                       from bd_psnalcust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                       left join bd_custcl cl on cust.pk_custcl = cl.pk_custcl
                       left join bd_custmodel el on cl.pk_custmodel =
                                                    el.pk_custmodel
                      where nvl(cust.sealflag, 'N') = 'N'
                        and nvl(cust.dr, '0') = '0'
                        and el.modelcode in ('02', '03')
                      group by son.pk_user) tgcount on son.pk_user =
                                                       tgcount.pk_user
          left join (select pk_user, count(pk_cust) counttgvisit
                       from (select hh.pk_user, hh.pk_cust
                               from bd_psnalcust cu
                               left join bd_custcl cl on cu.pk_custcl = cl.pk_custcl
                               left join bd_custmodel el on cl.pk_custmodel =
                                                            el.pk_custmodel
                               left join mb_psnalcustvisit_h hh on cu.pk_psnalcust =
                                                                   hh.pk_cust
                              where el.modelcode in ('02', '03')
                                and hh.pk_user is not null
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) tgvisit on son.pk_user = tgvisit.pk_user
          left join (select count(hh.pk_custvisit_h) conttgvisittime, hh.pk_user
                       from bd_psnalcust cus
                       left join bd_custcl cl on cus.pk_custcl = cl.pk_custcl
                       left join bd_custmodel el on cl.pk_custmodel =
                                                    el.pk_custmodel
                       left join mb_psnalcustvisit_h hh on cus.pk_psnalcust =
                                                           hh.pk_cust
                      where el.modelcode in ('02', '03')
                        and hh.pk_user is not null
                        and hh.vdate >= '2017-01-01'
        		        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) tgvisittime on son.pk_user =
                                                          tgvisittime.pk_user
          left join (select count(cust.pk_psnalcust) addtgcusts, son.pk_user
                       from bd_psnalcust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                       left join bd_custcl cl on cust.pk_custcl = cl.pk_custcl
                       left join bd_custmodel el on cl.pk_custmodel =
                                                    el.pk_custmodel
                      where el.modelcode in ('02', '03')
                        and cust.ts >= '2017-01-01'
        		        and cust.ts <= '2017-02-01'
                      group by son.pk_user) addtgcust on son.pk_user =
                                                         addtgcust.pk_user
          left join (select pk_user, count(pk_cust) adduptgvisits
                       from (select hh.pk_user, hh.pk_cust
                               from bd_psnalcust cu
                               left join bd_custcl cl on cu.pk_custcl = cl.pk_custcl
                               left join bd_custmodel el on cl.pk_custmodel =
                                                            el.pk_custmodel
                               left join mb_psnalcustvisit_h hh on cu.pk_psnalcust =
                                                                   hh.pk_cust
                              where el.modelcode in ('02', '03')
                                and hh.pk_user is not null
                                and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) adduptgvisit on son.pk_user =
                                                        adduptgvisit.pk_user
          left join (select count(hh.pk_custvisit_h) adduptgtimes, hh.pk_user
                       from bd_psnalcust cus
                       left join bd_custcl cl on cus.pk_custcl = cl.pk_custcl
                       left join bd_custmodel el on cl.pk_custmodel =
                                                    el.pk_custmodel
                       left join mb_psnalcustvisit_h hh on cus.pk_psnalcust =
                                                           hh.pk_cust
                      where el.modelcode in ('02', '03')
                        and hh.pk_user is not null
                        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) adduptgtime on son.pk_user =
                                                          adduptgtime.pk_user
          left join (select count(pk_cust) zdcounts, son.pk_user
                       from bd_cust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                      where cust.custprop = '1'
                        and nvl(cust.sealflag, 'N') = 'N'
                        and nvl(cust.dr, '0') = '0'
                      group by son.pk_user) zdcount on son.pk_user =
                                                       zdcount.pk_user
          left join (select pk_user, count(pk_cust) countzdvisit
                       from (select hh.pk_user, hh.pk_cust
                               from bd_cust cu
                              right join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                              where cu.custprop = '1'
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) zdvisit on son.pk_user = zdvisit.pk_user
          left join (select count(hh.pk_custvisit_h) contzdvisittime, hh.pk_user
                       from bd_cust cus
                      right join mb_custvisit_h hh on cus.pk_cust = hh.pk_cust
                      where cus.custprop = '1'
                        and hh.vdate >= '2017-01-01'
        		        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) zdvisittime on son.pk_user =
                                                          zdvisittime.pk_user
          left join (select count(cust.pk_cust) addzdcusts, son.pk_user
                       from bd_cust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                      where cust.custprop = '1'
                        and cust.ts >= '2017-01-01'
        		        and cust.ts <= '2017-02-01'
                      group by son.pk_user) addzdcust on son.pk_user =
                                                         addzdcust.pk_user
          left join (select pk_user, count(pk_cust) addupzdvisits
                       from (select hh.pk_user, hh.pk_cust
                               from bd_cust cu
                              right join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                              where cu.custprop = '1'
                                and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) addupzdvisit on son.pk_user =
                                                        addupzdvisit.pk_user
          left join (select count(hh.pk_custvisit_h) addupzdtimes, hh.pk_user
                       from bd_cust cus
                      right join mb_custvisit_h hh on cus.pk_cust = hh.pk_cust
                      where cus.custprop = '1'
                        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) addupzdtime on son.pk_user =
                                                          addupzdtime.pk_user
          left join (select count(pk_cust) Azdcounts, son.pk_user
                       from bd_cust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                       left join bd_custsize sizes on cust.pk_custsize =
                                                      sizes.pk_custsize
                      where cust.custprop = '1'
                        and sizes.custsizecode = '001'
                        and nvl(cust.sealflag, 'N') = 'N'
                        and nvl(cust.dr, '0') = '0'
                      group by son.pk_user) Azdcount on son.pk_user =
                                                        Azdcount.pk_user
          left join (select pk_user, count(pk_cust) Acountzdvisit
                       from (select hh.pk_user, hh.pk_cust
                               from bd_cust cu
                              right join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                               left join bd_custsize sizes on cu.pk_custsize =
                                                              sizes.pk_custsize
                              where cu.custprop = '1'
                                and sizes.custsizecode = '001'
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) Azdvisit on son.pk_user = Azdvisit.pk_user
          left join (select count(hh.pk_custvisit_h) Acontzdvisittime, hh.pk_user
                       from bd_cust cus
                      right join mb_custvisit_h hh on cus.pk_cust = hh.pk_cust
                       left join bd_custsize sizes on cus.pk_custsize =
                                                      sizes.pk_custsize
                      where cus.custprop = '1'
                        and sizes.custsizecode = '001'
                        and hh.vdate >= '2017-01-01'
        		        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) Azdvisittime on son.pk_user =
                                                           Azdvisittime.pk_user
          left join (select count(cust.pk_cust) Aaddzdcusts, son.pk_user
                       from bd_cust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                       left join bd_custsize sizes on cust.pk_custsize =
                                                      sizes.pk_custsize
                      where cust.custprop = '1'
                        and sizes.custsizecode = '001'
                        and cust.ts >= '2017-01-01'
        		        and cust.ts <= '2017-02-01'
                      group by son.pk_user) Aaddzdcust on son.pk_user =
                                                          Aaddzdcust.pk_user
          left join (select pk_user, count(pk_cust) Aaddupzdvisits
                       from (select hh.pk_user, hh.pk_cust
                               from bd_cust cu
                              right join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                               left join bd_custsize sizes on cu.pk_custsize =
                                                              sizes.pk_custsize
                              where cu.custprop = '1'
                                and sizes.custsizecode = '001'
                                and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) Aaddupzdvisit on son.pk_user =
                                                         Aaddupzdvisit.pk_user
          left join (select count(hh.pk_custvisit_h) Aaddupzdtimes, hh.pk_user
                       from bd_cust cus
                      right join mb_custvisit_h hh on cus.pk_cust = hh.pk_cust
                       left join bd_custsize sizes on cus.pk_custsize =
                                                      sizes.pk_custsize
                      where cus.custprop = '1'
                        and sizes.custsizecode = '001'
                        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) Aaddupzdtime on son.pk_user =
                                                           Aaddupzdtime.pk_user
          left join (select count(pk_cust) Bzdcounts, son.pk_user
                       from bd_cust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                       left join bd_custsize sizes on cust.pk_custsize =
                                                      sizes.pk_custsize
                      where cust.custprop = '1'
                        and sizes.custsizecode = '002'
                        and nvl(cust.sealflag, 'N') = 'N'
                        and nvl(cust.dr, '0') = '0'
                      group by son.pk_user) Bzdcount on son.pk_user =
                                                        Bzdcount.pk_user
          left join (select pk_user, count(pk_cust) Bcountzdvisit
                       from (select hh.pk_user, hh.pk_cust
                               from bd_cust cu
                              right join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                               left join bd_custsize sizes on cu.pk_custsize =
                                                              sizes.pk_custsize
                              where cu.custprop = '1'
                                and sizes.custsizecode = '002'
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) Bzdvisit on son.pk_user = Bzdvisit.pk_user
          left join (select count(hh.pk_custvisit_h) Bcontzdvisittime, hh.pk_user
                       from bd_cust cus
                      right join mb_custvisit_h hh on cus.pk_cust = hh.pk_cust
                       left join bd_custsize sizes on cus.pk_custsize =
                                                      sizes.pk_custsize
                      where cus.custprop = '1'
                        and sizes.custsizecode = '002'
                        and hh.vdate >= '2017-01-01'
        		        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) Bzdvisittime on son.pk_user =
                                                           Bzdvisittime.pk_user
          left join (select count(cust.pk_cust) Baddzdcusts, son.pk_user
                       from bd_cust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                       left join bd_custsize sizes on cust.pk_custsize =
                                                      sizes.pk_custsize
                      where cust.custprop = '1'
                        and sizes.custsizecode = '002'
                        and cust.ts >= '2017-01-01'
        		        and cust.ts <= '2017-02-01'
                      group by son.pk_user) Baddzdcust on son.pk_user =
                                                          Baddzdcust.pk_user
          left join (select pk_user, count(pk_cust) Baddupzdvisits
                       from (select hh.pk_user, hh.pk_cust
                               from bd_cust cu
                              right join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                               left join bd_custsize sizes on cu.pk_custsize =
                                                              sizes.pk_custsize
                              where cu.custprop = '1'
                                and sizes.custsizecode = '002'
                                and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) Baddupzdvisit on son.pk_user =
                                                         Baddupzdvisit.pk_user
          left join (select count(hh.pk_custvisit_h) Baddupzdtimes, hh.pk_user
                       from bd_cust cus
                      right join mb_custvisit_h hh on cus.pk_cust = hh.pk_cust
                       left join bd_custsize sizes on cus.pk_custsize =
                                                      sizes.pk_custsize
                      where cus.custprop = '1'
                        and sizes.custsizecode = '002'
                        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) Baddupzdtime on son.pk_user =
                                                           Baddupzdtime.pk_user
          left join (select count(pk_cust) Czdcounts, son.pk_user
                       from bd_cust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                       left join bd_custsize sizes on cust.pk_custsize =
                                                      sizes.pk_custsize
                      where cust.custprop = '1'
                        and sizes.custsizecode = '003'
                        and nvl(cust.sealflag, 'N') = 'N'
                        and nvl(cust.dr, '0') = '0'
                      group by son.pk_user) Czdcount on son.pk_user =
                                                        Czdcount.pk_user
          left join (select pk_user, count(pk_cust) Ccountzdvisit
                       from (select hh.pk_user, hh.pk_cust
                               from bd_cust cu
                              right join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                               left join bd_custsize sizes on cu.pk_custsize =
                                                              sizes.pk_custsize
                              where cu.custprop = '1'
                                and sizes.custsizecode = '003'
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) Czdvisit on son.pk_user = Czdvisit.pk_user
          left join (select count(hh.pk_custvisit_h) Ccontzdvisittime, hh.pk_user
                       from bd_cust cus
                      right join mb_custvisit_h hh on cus.pk_cust = hh.pk_cust
                       left join bd_custsize sizes on cus.pk_custsize =
                                                      sizes.pk_custsize
                      where cus.custprop = '1'
                        and sizes.custsizecode = '003'
                        and hh.vdate >= '2017-01-01'
        		        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) Czdvisittime on son.pk_user =
                                                           Czdvisittime.pk_user
          left join (select count(cust.pk_cust) Caddzdcusts, son.pk_user
                       from bd_cust cust
                       left join bd_person son on cust.pk_psn = son.pk_psn
                       left join bd_custsize sizes on cust.pk_custsize =
                                                      sizes.pk_custsize
                      where cust.custprop = '1'
                        and sizes.custsizecode = '003'
                        and cust.ts >= '2017-01-01'
        		        and cust.ts <= '2017-02-01'
                      group by son.pk_user) Caddzdcust on son.pk_user =
                                                          Caddzdcust.pk_user
          left join (select pk_user, count(pk_cust) Caddupzdvisits
                       from (select hh.pk_user, hh.pk_cust
                               from bd_cust cu
                              right join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                               left join bd_custsize sizes on cu.pk_custsize =
                                                              sizes.pk_custsize
                              where cu.custprop = '1'
                                and sizes.custsizecode = '003'
                                and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, hh.pk_cust)
                      group by pk_user) Caddupzdvisit on son.pk_user =
                                                         Caddupzdvisit.pk_user
          left join (select count(hh.pk_custvisit_h) Caddupzdtimes, hh.pk_user
                       from bd_cust cus
                      right join mb_custvisit_h hh on cus.pk_cust = hh.pk_cust
                       left join bd_custsize sizes on cus.pk_custsize =
                                                      sizes.pk_custsize
                      where cus.custprop = '1'
                        and sizes.custsizecode = '003'
                        and hh.vdate <= '2017-02-01'
                      group by hh.pk_user) Caddupzdtime on son.pk_user =
                                                           Caddupzdtime.pk_user
          left join (select pk_user, count(pk_custvisit_h) phcounts
                       from (select hh.pk_user, bb.pk_custvisit_h
                               from bd_cust cu
                               left join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                               left join mb_custvisit_b bb on hh.pk_custvisit_h =
                                                              bb.pk_custvisit_h
                               left join bd_selfdef_b def on bb.pk_selfdef_b =
                                                             def.pk_selfdef_b
                              where def.enumname = '已铺货'
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, bb.pk_custvisit_h)
                      group by pk_user) ph on son.pk_user = ph.pk_user
          left join (select pk_user, count(pk_custvisit_h) nophcounts
                       from (select hh.pk_user, bb.pk_custvisit_h
                               from bd_cust cu
                               left join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                               left join mb_custvisit_b bb on hh.pk_custvisit_h =
                                                              bb.pk_custvisit_h
                               left join bd_selfdef_b def on bb.pk_selfdef_b =
                                                             def.pk_selfdef_b
                              where def.enumname = '无铺货'
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, bb.pk_custvisit_h)
                      group by pk_user) noph on son.pk_user = noph.pk_user
          left join (select pk_user, count(pk_custvisit_h) dxcounts
                       from (select hh.pk_user, bb.pk_custvisit_h
                               from bd_cust cu
                               left join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                               left join mb_custvisit_b bb on hh.pk_custvisit_h =
                                                              bb.pk_custvisit_h
                               left join bd_selfdef_b def on bb.pk_selfdef_b =
                                                             def.pk_selfdef_b
                              where def.enumname = '已动销'
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, bb.pk_custvisit_h)
                      group by pk_user) dx on son.pk_user = dx.pk_user
          left join (select pk_user, count(pk_custvisit_h) nodxcounts
                       from (select hh.pk_user, bb.pk_custvisit_h
                               from bd_cust cu
                               left join mb_custvisit_h hh on cu.pk_cust = hh.pk_cust
                               left join mb_custvisit_b bb on hh.pk_custvisit_h =
                                                              bb.pk_custvisit_h
                               left join bd_selfdef_b def on bb.pk_selfdef_b =
                                                             def.pk_selfdef_b
                              where def.enumname = '无动销'
                                and hh.vdate >= '2017-01-01'
        			            and hh.vdate <= '2017-02-01'
                              group by hh.pk_user, bb.pk_custvisit_h)
                      group by pk_user) nodx on son.pk_user = nodx.pk_user
         where
           son.pk_user is not null
           and nvl(son.sealflag, 'N') = 'N'
         group by son.pk_corp, dept.deptname, son.psnname, cl.psnclname

                '''
        start_date = time.time()
        ss = self.db.executemany(sql)
        end_date = time.time()
        return end_date - start_date