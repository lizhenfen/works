from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json

es = Elasticsearch(['192.168.15.212:9200'])



def group_by_employee(index,start_date=None,end_date=None,doc_type="custvisit",size=10,interval=False):
    interval_time = "minute" if interval else "day"
    req = {
        "query": {
            "bool": {
                "filter": {"range": {"VDATE": {"gte": start_date, "lte": end_date,"format": "yyyy/MM/dd"}}}
            }
        },
        "aggs": {
            "groups": {
                "date_histogram": {"field": "VDATE", "interval": interval_time},
                "aggs": {"by_user": {"terms": {"field": "PK_USER"}}}
            }
        }
    }
    data = es.search(index=index, doc_type=doc_type, body=json.dumps(req))
    return data["aggregations"]["groups"]["buckets"]


def search_by_tuan(index,size=1):
    req = {
        "size": 1,
        "query":{
            "bool": {
                "must":{
                    "match":{"PK_PSNALCUST":"20150301-B83A-F00C-4E05-3ACA8006500C"}
                },
            }
        },
    }
    data = es.search(index=index, doc_type="bd_psnalcust", body=json.dumps(req))
    return data


def search_key(index,size=10,start_date=None,end_date=None,key="PK_USER",doc_type="custvisit",
               person_name=None,company_name=None):
    req = {
        "query": {
            "bool": {
                "filter": {"range": {"VDATE": {"gte": start_date, "lte": end_date,"format": "yyyy/MM/dd"}}}
            }
        },
        "aggs": {
            "by_day":{
                "date_histogram":{"field": "VDATE","interval":"day"},
                "aggs":{"by_user":{"terms":{"field":key}}}
            }
        }
    }
    if company_name:
        req["query"]["bool"]["must"] =  {"term": {"PK_CORP": company_name }},
    if person_name:
        must = {"match": {"PSNAME": person_name}}
        req["query"]["bool"]["must"] = must
    data = es.search(index=index, doc_type=doc_type, body=json.dumps(req))
    return data["aggregations"]["by_day"]["buckets"]


def search_by_date(index="test-index",start_date=None, doc_type="custvisit",end_date=None,
                   key="PSNAME",company_name=None,person_name=None):
    # 存在一个小BUG, 当用户重名时，需要根据PK_USER分组
    req = {
        "size": 10,
        "_source": "false",
        "query": {
            "bool": {
                "filter": {"range": {"VDATE": {"gte": start_date, "lte": end_date, "format": "yyyy/MM/dd"}}}
            }
        },
        "aggs": {
            "groups": {
                "terms": {"field": key , "size": 6*1024*1024}}
        }
    }
    if company_name:
        req["query"]["bool"]["must"] =  {"term": {"PK_CORP": company_name }}
    if person_name:
        must = {"match": {"PSNAME": person_name}}
        req["query"]["bool"]["must"] = must
    res = es.search(index=index, doc_type=doc_type, body=json.dumps(req))

    return res["aggregations"]["groups"]


def search_by_pdcust(index="test-index",doc_type='pdcust',key=None, custtype=None):
    req = {
        "query": {
            "bool": {
                "must": {
                    "match": {"PK_CUST": key},
                },
            }
        }
    }
    data = es.search(index=index, doc_type=doc_type, body=json.dumps(req))
    try:
        res = data['hits']['hits'][0]["_source"]["CUSTPROP"]
        print(res)
    except:
        res = None

    return res

#统计拜访数据
def search_by_cust_id(index,start_date=None,end_date=None,size=10,key="PK_USER",company=None):
    '''
        根据客户类型: 0,1 区分
    '''
    req = {
        "size": 1,
        "_source": "false",
        "query":{
            "bool": {
                "filter": {"range": {"VDATE": {"lte": end_date, "gte": start_date, "format": "yyyy/MM/dd"}}}
            }
        },

        "aggs": {
            "groups": {
                # 此值用来根据姓名或PK_USER 排序
                "terms":{"field": "PSNAME" , "size": 6 * 1024 * 1024},
                "aggs": {"by_user": {"terms": {"field": "PK_CORP_ID"},
                                     "aggs":{"unique": {"cardinality": {"field": "PK_CUST" }}},
                         },
            },
        }
    }}
    if company:
        req["query"]["bool"]["must"] =  {"term": {"PK_CORP": company }},

    data = es.search(index=index,body=req)
    count = data["hits"]["total"]
    res = data["aggregations"]["groups"]
    res["count"] = count
    return res


def test(index,size=10,start_date=None,end_date=None,doc_type="mb_report"):
    '''根据 search_key 改编'''
    req = {
        "size": 100,
        "query": {
            "bool": {
                "filter": {"range": {"VDATE": {"gte": start_date, "lte": end_date,"format": "yyyy/MM/dd HH:mm"}}}
            }
        },
        "sort": {
            "VDATE": {"order": "asc"}
        },
        "aggs": {
            "by_day":{
                "date_histogram":{"field": "VDATE","interval":"30m"},
            }
        }
    }

    data = es.search(index=index, doc_type=doc_type, body=json.dumps(req))
    return data


if __name__ == "__main__":

    import time
    start_time = time.time()
    res = test("test-index", size=10, start_date="2017/03/11 00:00",
                       end_date="2017/03/12 11:00",
                       doc_type="mb_report")
    print(res)
