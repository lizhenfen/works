from __future__ import absolute_import

from comm import database

def relationMap():
    sql = '''
             select a.pk_user,a.psnname, nvl(cust0.dearlernum,0) dearlernum, nvl(cust1.custnum,0) custnum, nvl(cust2.psnalnum,0) psnalnum
            from bd_person a
            left join (select a.pk_corp, a.pk_psn, count(a.pk_cust) dearlernum
            from v_dealersandcust a
            where a.custprop = 0
            group by a.pk_corp, a.pk_psn) cust0 on a.pk_corp = cust0.pk_corp and a.pk_psn = cust0.pk_psn
            left join (select a.pk_corp, a.pk_psn, count(a.pk_cust) custnum
            from v_dealersandcust a
            where a.custprop = 1
            group by a.pk_corp, a.pk_psn) cust1 on a.pk_corp = cust1.pk_corp and a.pk_psn = cust1.pk_psn
            left join (select b.pk_corp, b.pk_psn, count(b.pk_psnalcust) psnalnum
            from bd_psnalcust b
            group by b.pk_corp, b.pk_psn) cust2 on a.pk_corp = cust2.pk_corp and a.pk_psn = cust2.pk_psn

                 '''
    t = database.Connection()
    ss = t.executemany(sql)
    relationship = {}
    for i in ss:
        #if i[-1] == 0 and i[-2] == 0 and i[-3] == 0:
        #    continue
        relationship[i[0]] = (i[1], i[2], i[3], i[4])
    #print(relationship)
    return relationship

relationship = relationMap()