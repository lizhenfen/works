import time
import cx_Oracle
import redis
import json

version = "0.1"
version_info = (0,1,0,0)

class Connection(object):
    def __init__(self,host=None,database=None,user=None,password=None,max_idle_time=7*3600,
                 connection_timeout=0,time_zone="+0:00", charset="utf8"):
        self._db = None
        self.max_idle_time = max_idle_time
        self._last_use_time= time.time()
        try:
            self.reconnect()
        except Exception as e:
            raise Exception("数据库连接失败",e)

    def __del__(self):
        self.close()

    def close(self):
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        self.close()
        self._db = cx_Oracle.connect('jlfmmp','jlfmmptest','192.168.15.66/hzdb66')

    def _ensure_connected(self):
        if (self._db is None or
                (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, parameters, kwparameters):
        try:
            return cursor.execute(query, kwparameters or parameters)
        except Exception as e:
            self.close()
            raise

    def get(self, query, *parameters, **kwparameters):
        """Returns the (singular) row returned by the given query.

        If the query has no results, returns None.  If it has
        more than one result, raises an exception.
        """
        rows = list(self.query(query, *parameters, **kwparameters))
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    def query(self,query, *parameter, **kwparameters):
        cursor = self._cursor()
        try:
            self._execute(cursor,query, parameter, kwparameters)
            column_names = [ d[0] for d in cursor.description ]
            for row in cursor:
                yield Row(zip(column_names,row))
        finally:
            cursor.close()


    def execute_lastrowid(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.fetchall()
        finally:
            cursor.close()

    def executemany(self, query, *parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        return self.execute_lastrowid(query, *parameters)

class Row(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return AttributeError(name)



class RedisConn(object):
    def __init__(self):
        try:
            self.reconnect()
        except Exception as e:
            raise Exception("redis 连接失败", str(e))

    def reconnect(self):
        self.rs = redis.Redis(host='192.168.15.212',port=6379, db=1)

    def __del__(self):
        if getattr(self,'rs',None) is not None:
            self.rs = None

    def  set(self,k,v):
        self.rs.set(k,v)

    def get(self, k):
        return self.rs.get(k)

if __name__ == "__main__":

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
    t = Connection()
    ss = t.executemany(sql)
    relationship = {}
    rds  = RedisConn()
    '''for i in ss:
        # if i[-1] == 0 and i[-2] == 0 and i[-3] == 0:
        #    continue
        rds.set(i[0],json.dumps([i[1], i[2], i[3], i[4]]))
        print(i)
    '''
    print(rds.get('E634BB00-700D-11E6-BB0F-F62BD1B9EB67').decode())