from elasticsearch import Elasticsearch
import json


es = Elasticsearch(['10.0.0.3:9200'])


def group_by_company(index,start_date=None,end_date=None,doc_type="custvisit",size=10,key="PK_USER"):
    req = {
        "_source": "false",
        "query":{
            "bool":{
                "filter":{"range":{"VDATE":{"lte": end_date,"gte": start_date,"format":"yyyy/MM/dd"}}}
            }
        },
            "aggs": {"groups": {"terms": {"field": key,"size": size}},},
    }
    data = es.search(index=index,doc_type=doc_type,body=req)
    return data["aggregations"]["groups"]


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


def search_key(index,size=10,start_date=None,end_date=None,key="PK_USER",doc_type="custvisit",person_name=None):
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
    if person_name:
        must = {"match": {"PK_USER": person_name}}
        req["query"]["bool"]["must"] = must
    data = es.search(index=index, doc_type=doc_type, body=json.dumps(req))
    return data["aggregations"]["by_day"]["buckets"]


def search_by_date(index="test-index",start_date=None, doc_type="custvisit",end_date=None,key="PK_USER",size=10):
    req = {
        "size": size,
        "query": {
            "bool": {
                "filter": {"range": {"VDATE": {"gte": start_date, "lte": end_date, "format": "yyyy/MM/dd"}}}
            }
        },
        "aggs": {
            "groups": {
                "terms": {"field": key }}
        }
    }
    res = es.search(index=index, doc_type=doc_type, body=json.dumps(req))

    return res


def search_by_pdcust(index="test-index",doc_type='pdcust',key=None):
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
    except:
        res = None

    return res

def search_by_cust_id(index,start_date=None,end_date=None,size=10,key="PK_USER"):
    '''
        根据客户类型: 0,1 区分
    '''
    req = {
        "size": size,
        "_source": "false",
        "query":{
            "bool":{

                "filter":{"range":{"VDATE":{"lte": end_date,"gte": start_date,"format":"yyyy/MM/dd"}}}
            }
        },
        "aggs": {
            "groups": {
                "terms":{"field": "%s" % key,"size": size},
                "aggs": {"by_user": {"terms": {"field": "PK_CORP_ID"}}}
            },}
    }


    data = es.search(index=index,body=req)
    return data["aggregations"]["groups"]

def test(index,size=10,start_date=None,end_date=None,doc_type="mb_report"):
    '''根据 search_key 改编'''
    req = {
        "query": {
            "bool": {

                "filter": {"range": {"VDATE": {"gte": start_date, "lte": end_date,"format": "yyyy/MM/dd HH:mm"}}}
            }
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
    '''
    res = search_by_date("test-index",
                         start_date="2017/02/11",
                         end_date="2017/02/11",
                         doc_type="mb_report",  key="PK_USER")
    '''
    res = test("test-index", size=10, start_date="2017/02/11 00:00",
               end_date="2017/02/11 10:00", doc_type="mb_report")
    end_time = time.time()
    seconds = end_time - start_time
    print(res)
    print(seconds)