from elasticsearch import Elasticsearch
import csv
import json
import elasapi
import time

es = Elasticsearch(['10.0.0.3:9200'])

def create_index(index="test-index"):
    #创建索引
    data = {
        "mappings":{
            "custvisit": {
                "properties": {
                    "PK_CUSTVISIT_H":{"type": "string","index": "not_analyzed"},
                    "PK_CUST":{"type": "string","index": "not_analyzed"},
                    "PK_CORP":{"type": "string","index": "not_analyzed"},
                    "VDATE":{"type": "date","index": "not_analyzed",
                            "format": "yyyy/MM/dd HH:mm"},
                    "PK_USER":{"type": "string","index": "not_analyzed"},
                    "PK_CORP_ID":{"type": "string","index": "not_analyzed"}
                }
            },

        }
    }
    es.indices.create(index=index,
                      body=json.dumps(data),
                      ignore=[400])

def convert_date(src_date):
    t = time.strptime(src_date, "%Y-%m-%d %H:%M:%S")
    convert_d = time.strftime("%Y/%m/%d %H:%M", t)
    return convert_d

def insert_data(path,index="test-index",doc_type="custvisit",convert_d=False):
    #插入索引
    with open(path, "r") as f:
        # filednames= [xx,yy,]  此关键字用于指定字典的key, 若未指定，默认使用第一个关键字
        reader = csv.DictReader(f)
        for line in reader:
            if convert_d:
                line["VDATE"] = convert_date(line["VDATE"])
            data = json.dumps(line)
            es.index(index=index,doc_type=doc_type,body=data)

def del_index(index="test-index"):
    es.indices.delete(index=index)

def insert_mb_custvisi_h(path,index,doc_type="custvisit"):
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            key = line["PK_CUST"]
            keys = elasapi.search_by_pdcust(index="test-index",doc_type='pdcust',key=key)
            if not keys: continue
            line["PK_CORP_ID"] = str(keys)
            data = json.dumps(line)
            print(data)
            es.index(index=index,doc_type=doc_type,body=data)

def insert_mb_report(path,index="test-index",doc_type="mb_report"):
    with open(path, "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        for line in reader:
            line["REPORTADDR"] = line["REPORTADDR"]
            data = json.dumps(line)
            print(data)
            es.index(index=index,doc_type=doc_type,body=data)

if __name__ == "__main__":
    #del_index(index="test-index")
    #创建索引
    #create_index()
    #插入客户档案
    #insert_data("bd_cust.csv",index="test-index",doc_type="pdcust")
    #insert_data("t1.csv",index="test-index",doc_type="pdcust")
    #插入客户拜访记录
    '''insert_child_data("mb_custvisit_h.csv",
                index="test-index",
                doc_type="custvisit",
                )
    '''
    #导入客户拜访记录
    #insert_mb_custvisi_h(r"C:\Users\Administrator\Desktop\three\mb_custvisit_h.csv",index="test-index",doc_type="custvisit")
    #导入开始工作时间、
    insert_mb_report(r'C:\Users\Administrator\Desktop\three\mb_reportinfo2.csv')
