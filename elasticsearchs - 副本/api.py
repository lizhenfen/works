from elasticsearch import Elasticsearch
import csv
import json

es = Elasticsearch(['10.0.0.3:9200'])
'''
#创建索引
data = {
    "mappings":{
        "custvisit": {
            "properties": {
                "PK_CUSTVISIT_H":{"type": "string","index": "not_analyzed"},
                "PK_CUST":{"type": "string","index": "not_analyzed"},
                "PK_CORP":{"type": "string","index": "not_analyzed"},
                "VDATE":{"type": "string","index": "not_analyzed"},
                "PK_USER":{"type": "string","index": "not_analyzed"},
            }
        }
    }
}
es.indices.create(index="test-index", body=json.dumps(data),ignore=[400])
'''

'''
#插入索引
with open("mb_custvisit_h.csv", "r") as f:
    # filednames= [xx,yy,]  此关键字用于指定字典的key, 若未指定，默认使用第一个关键字
    reader = csv.DictReader(f)
    for line in reader:
        #print(line)
        data = json.dumps(line)
        print(data, type(data))
        es.index(index="test-index",doc_type="custvisit",body=data)


es.search(index="test-index", filter_path=['hits.hits._id', 'hits.hits._type'])
#es.indices.delete(index="test-index")
'''

'''
获取分组数据
curl -XPOST http://10.0.0.3:9200/test-index/_search?pretty -d '{"size": 0,"aggs":{"group_by_state":{"terms":{"field":"PK_USER"}}}}'
'''
data ={
    "size": 0,
    "aggs": {
      "group_by_state": {
        "terms": {
          "field": "PK_USER"
        }
      }
    }
    }
print(es.search(index="test-index", doc_type="custvisit",
                    body=data))