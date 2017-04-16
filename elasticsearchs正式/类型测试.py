from elasticsearch import Elasticsearch
import json

es = Elasticsearch(["10.0.0.3:9200"])

index = {
    "mappings": {
        "user":{
            "properties":{
                "uid": {"type": "string","index": "not_analyzed"},
                "name": {"type": "string", "index": "not_analyzed"},
                "birth": {"type": "date", "index":"not_analyzed"}
            }
        },
        "compute":{
            "properties":{
                "uid": {"type": "string","index": "not_analyzed"},
                "cname": {"type": "string", "index": "not_analyzed"}
            }
        }
    }
}
#es.indices.create(index="t1", body=json.dumps(index))
user =[
    {"uid": "1",
    "name": "lz",
    "birth": "1990-09-07"},
    {"uid": "2",
    "name": "lh",
    "birth": "1990-09-08"},
    {"uid": "3",
    "name": "hn",
    "birth": "1990-10-08"},
]
com = [
    {"uid": "1",
     "cname": "jlf"},
    {"uid": "2",
     "cname": "jf"},
    {"uid": "3",
     "cname": "lf"},
]

'''
for u in user:
    es.index(index="t1",doc_type="user", body=u)
for c in com:
    es.index(index="t1",doc_type="com", body=c)
'''
search = {
    "size": 1,

    "aggs": {"grp_by_com": {"terms": {"field":"uid"}}}

}
data = es.search(index="t1",body=search)
print(json.dumps(data, indent=4))