data = [
        {'doc_count': 225, 'key': '李贵海', 'by_user': {'sum_other_doc_count': 0, 'doc_count_error_upper_bound': 0, 'buckets': [{'unique': {'value': 96}, 'doc_count': 225, 'key': '1'}]}}, 
        {'doc_count': 216, 'key': '杨吉利', 'by_user': {'sum_other_doc_count': 0, 'doc_count_error_upper_bound': 0, 'buckets': [{'unique': {'value': 98}, 'doc_count': 216, 'key': '1'}]}}, 
        {'doc_count': 214, 'key': '田磊', 'by_user': {'sum_other_doc_count': 0, 'doc_count_error_upper_bound': 0, 'buckets': [{'unique': {'value': 166}, 'doc_count': 214, 'key': '1' }]}} 
    ]

def valueMap(res):
    res = res["by_user"]["buckets"]
    all_keys = [0,1,2]
    if len(res) <= 3:
        key = [ k["key"] for k in res ]
        no_keys = list(set(all_keys) - set(key) )
    res.extend([ {'doc_count': 0, 'unique': {'value': 0}, 'key': _ }  for _ in no_keys ])
    return res
    

#t = valueMap(data)
rs = map(valueMap, data)
print( list(rs) )
