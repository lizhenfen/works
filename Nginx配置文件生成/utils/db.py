#!/usr/bin/env python
#-*- coding: utf8 -*-

try:
    import MySQLdb
except:
    import pymysql as MySQLdb
import time


class Connection(object):
    def __init__(self, host, database, user=None, password=None,
                 max_idle_time=7*3600, connect_timeout=0,
                 time_zone="+0:00", charset="utf8",sql_mode="TRADOTIONAL")
        self.host = host
        self.database = database
        self.max_idle_time = float(max_idle_time)
        args = dict(conv=CONVERSIONS, use_unicode=True, charset=charset,db=database,
                    init_command=('set time_zone=%s' % time_zone), 
                    connect_timeout=connect_timeout, sql_mode=sql_mode)
        if user is not None:
            args['user'] = user
        if password is not None:
            args['password'] = password
        if '/' in self.host:
            args['unix_socket'] = host
        else:
            self.socket = None
            pair = self.host.split(":")
            if len(pair) == 2:
                args['host'] = pair[0]
                args['port'] = int(pair[1])
            else:
                args['host'] = host
                args['port'] = 3306
        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception as e:
            #此处记录连接失败日志
            pass
            
    def __del__(self):
        self.close()
        
    def close(self):
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None
            
    def reconnect(self):
        self.close()
        self._db = MySQLdb.connect(**self._db_args)
        self._db.autocommit(True)
    
    def iter(self, query, *args, **kwargs):
        self._ensure_connected()
        cursor = MySQLdb.cursors.SSCursor(self._db)
        try:
            self._execute(cursor, query, *args, **kwargs)
            column_name = [ d[0] for d in cursor.description ]
            for row in cursor:
                yield Row(zip(column_name, row))
        finally:
            cursor.close()
            
    def query(self, query, *args, **kwargs):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, args, kwargs)
            column_name = [ d[0] for d in cursor.description ]
            return [Row(zip(column_name, row)) for row in cursor ]
        finally:
            cursor.close()

    def get(self, query, *args, **kwargs):
        rows =self.query()
    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()
        
    def _execute(self, cursor, query, args, kwargs):
        try:
            return cursor.execute(query, kwargs or args)
        except OptionalError as e:
            #此处记录查询错误日志
            self.close()
            raise
            
    def _ensure_connected(self):
        if (self._db is None or
            time.time() - self._last_use_time > self.max_idle_time):
            self.reconnect()
        self._last_use_time = time.time()
    
class Row(dict):
    #把元组装饰成字典
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
            
connect = MySQLdb.connect(host="192.168.15.39",port=3306,
                          user="lz",password="lz",
                          database='test')
connect.select_db('test')
cursor = connect.cursor()
cursor.execute('select * from nginx_prx')
data = cursor.fetchall()
print(data)