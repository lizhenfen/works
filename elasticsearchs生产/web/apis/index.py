import tornado.web
from comm import elasapi
from comm import common
from tornado.escape import json_encode
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import tornado.gen

class APIIndexClassCountByCustom(tornado.web.RequestHandler):

    def convert_key(self,k):
        if k['name'] == '1':
            k['name'] = '网点'
        if k['name'] == '2':
            k['name'] = '团购'
        if k['name'] == '3':
            k['name'] = '经销商'
        return k

    def post(self, *args, **kwargs):
        first_day, end_day = common.getMonthFirstDayAndLastDay()
        res = elasapi.search_by_date(index="test-index",
                             start_date= first_day,
                             doc_type="custvisit",
                             end_date=end_day,
                             key="PK_CORP_ID", )
        res = [ {'name': k['key'],'value': k['doc_count'] } for k in res['buckets'] ]
        list(map(self.convert_key, res ))
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.finish(json_encode(res))


class APIIndexAllCount(tornado.web.RequestHandler):
    corp_name = {}  # 缓存公司对应关系
    def convert_corp_name(self,cname):
        if not self.corp_name.get(cname["key"],None):
            company = elasapi.person_to_company('%s' % cname["key"])
            self.corp_name[ cname["key"] ] = company
        cname["key"] = self.corp_name.get(cname["key"],'未知')
        return cname
    def convert_v_to_k(self, convert_list):
        res = {}
        for _ in convert_list:
            res[_['key']] = _['doc_count']
        return res
    def convert_key(self,k):
        if k['key'] == '1':
            k['key'] = '网点'
        if k['key'] == '2':
            k['key'] = '团购'
        if k['key'] == '3':
            k['key'] = '经销商'
        return k

    def post(self, *args, **kwargs):
        res_dict = {}
        #first_day, end_day = common.getMonthFirstDayAndLastDay()
        first_day = '2017/04/01'
        end_day   = '2017/04/30'
        company = elasapi.search_by_date(index="test-index",
                         start_date=first_day,
                         doc_type="custvisit",
                         end_date=end_day,
                         key="PK_CORP", )
        list(map( self.convert_corp_name,company['buckets'] ))
        res_dict['company'] = self.convert_v_to_k(company['buckets'])

        class_customer = elasapi.search_by_date(index="test-index",
                                     start_date=first_day,
                                     doc_type="custvisit",
                                     end_date=end_day,
                                     key="PK_CORP_ID", )
        list(map(self.convert_key, class_customer['buckets']))
        class_customer = self.convert_v_to_k(class_customer['buckets'])
        res_dict['class_customer'] = class_customer
        res_dict['all'] = sum([ class_customer[k] for k in class_customer ])

        self.write(json_encode(res_dict))