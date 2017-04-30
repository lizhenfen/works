from elasticsearch import Elasticsearch
import csv
import json
import elasapi
import time
import database

es = Elasticsearch(['192.168.15.212:9200'])


# 创建拜访记录索引
def create_index(index="test-index"):
    # 创建索引
    data = {
        "mappings": {
            "custvisit": {
                "properties": {
                    "PK_CUSTVISIT_H": {"type": "string", "index": "not_analyzed"},
                    "PK_CUST": {"type": "string", "index": "not_analyzed"},
                    "PK_CORP": {"type": "string", "index": "not_analyzed"},
                    "VDATE": {"type": "date", "index": "not_analyzed",
                              "format": "yyyy/MM/dd HH:mm:ss"},
                    "PK_USER": {"type": "string", "index": "not_analyzed"},
                    "PK_CORP_ID": {"type": "string", "index": "not_analyzed"},
                    "PSNAME": {"type": "string", "index": "not_analyzed"}
                }
            },

        }
    }
    es.indices.create(index=index,
                      body=json.dumps(data),
                      ignore=[400])

# 转换日期格式
def convert_date(src_date):
    try:
        t = time.strptime(src_date, "%Y-%m-%d %H:%M:%S")
    except:
        t = time.strptime(src_date, "%Y-%m-%d %H:%M")
        t = t + ":00"
    convert_d = time.strftime("%Y/%m/%d %H:%M:%S", t)
    return convert_d


# 基础数据插入函数,
# 主要用于插入前置数据数据,, 用户拜访的一般客户类型(bd_cust), 团购客户类型(bd_psnalcust)
def insert_data(sql, index="test-index", doc_type="pdcust", convert_d=False):
    '''
        convert_d: 是否转换日期格式, 当前不需要传入此值, 暂时放弃
    '''

    # 通过数据库直接传入数据拜访数据
    db = database.Connection()
    ss = db.query(sql)
    for line in ss:
        if convert_d:
            line["VDATE"] = convert_date(line["VDATE"].strip())
        print(line)
        es.index(index=index, doc_type=doc_type, body=line)


# 删除索引
def del_index(index="test-index"):
    es.indices.delete(index=index)


# 导入供应商, 网点的拜访记录
def insert_mb_custvisi_h(sql, index="test-index", doc_type="custvisit"):
    '''
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            key = line["PK_CUST"]
            keys = elasapi.search_by_pdcust(index="test-index", doc_type='pdcust', key=key)
            if not keys: continue
            line["PK_CORP_ID"] = str(keys)
            line["VDATE"] = convert_date(line["VDATE"].strip())
            data = json.dumps(line)
            print(data)
            es.index(index=index, doc_type=doc_type, body=data)
    '''
    username_sql = '''
          select a.pk_corp, a.pk_psn, a.psnname, a.pk_user
          from bd_person a
          where  a.pk_corp<>'3EA0CF10-FB39-11E2-8F10-C7A1C15F563D' and a.pk_user = :1
          '''
    db = database.Connection()
    ss = db.query(sql)
    for line in ss:
        key = line["PK_CUST"]
        keys = elasapi.search_by_pdcust(index="test-index", doc_type='pdcust', key=key,custtype=2)
        if not keys: continue
        try:
            username = db.get(username_sql,line["PK_USER"])
        except:
            # PK_SER 有多个值
            continue
        if username:
            line["PSNAME"] = username["PSNNAME"]
        line["PK_CORP_ID"] = str(keys)
        line["VDATE"] = convert_date(line["VDATE"].strip())
        data = json.dumps(line)
        print(data)
        es.index(index=index, doc_type=doc_type, body=data)


# 导入开始工作时间
def insert_mb_report(sql, index="test-index", doc_type="mb_report"):
    '''
    with open(path, "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        for line in reader:
            line["REPORTADDR"] = line["REPORTADDR"]
            data = json.dumps(line)
            print(data)
            es.index(index=index, doc_type=doc_type, body=data)
    '''
    person_sql = '''
                        select  a.psnname
                        from bd_person a
                        where a.pk_user=:1 '''

    db = database.Connection()
    ss = db.query(sql)
    for line in ss:
        line["VDATE"] = convert_date(line["VDATE"].strip())
        try:
            line["PSNNAME"] = db.get(person_sql, line["PK_USER"])["PSNNAME"]
        except:
            continue
        data = json.dumps(line)
        print(data)
        es.index(index=index, doc_type=doc_type, body=data)


if __name__ == "__main__":
    del_index(index="test-index")
    # 创建索引
    create_index()
    # 导入经销商(0)、网点(1)客户档案
    company_sql = '''
                        select cust.pk_corp,cust.pk_cust,cust.pk_psn,nvl(cust.custprop,1) custprop
                        from v_dealersandcust cust
                        where cust.custprop != 2


                    '''
    insert_data(company_sql)

    # 导入团购(2)客户档案
    tuangou_sql = '''
                              select a.pk_corp, a.pk_psnalcust pk_cust, a.pk_psn, '2' custprop
                              from bd_psnalcust a

                        '''
    insert_data(tuangou_sql)

    # 导入客户的经销商, 网点拜访明细
    kehu_baifang_sql = '''
                                                select a.pk_custvisit_h, a.pk_corp, a.pk_user, a.vdate, a.pk_cust
                                                from mb_custvisit_h a
                                                where a.vdate >= '2017-01-01'
                                                                    and a.vdate <= '2017-04-02'
                                         '''
    insert_mb_custvisi_h(kehu_baifang_sql, index="test-index", doc_type="custvisit")

    # 导入团购拜访明细
    tuangou_baifang_sql = '''
                                 select b.pk_custvisit_h, b.pk_corp, b.pk_user, b.vdate, b.pk_cust
                                 from mb_psnalcustvisit_h b
                                 WHERE  b.vdate >= '2017-01-01'
                                                    and b.vdate <= '2017-04-01'
                         '''
    insert_mb_custvisi_h(tuangou_baifang_sql, index="test-index", doc_type="custvisit")

    # 导入开始工作时间、
    work_sql = '''
            select pk_reportinfo, pk_corp, pk_user, reporttime as vdate, reportaddr
            from mb_reportinfo

                             and  reporttime >= '2017-01-01'
                             and  reporttime <= '2017-04-04'
        '''
    insert_mb_report(work_sql, index="test-index", doc_type="mb_report")

    # 导入公司信息
    company_name_sql = '''
            select a.corp_id,a.unitname from pub_corp a
        '''
    insert_data(company_name_sql, index="test-index", doc_type="company")

    # 导入个人信息
    company_name_sql = '''
            select a.pk_corp, a.pk_psn, a.psnname, a.pk_user
            from bd_person a
        '''
    insert_data(company_name_sql, index="test-index", doc_type="person")