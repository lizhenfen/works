import tornado.web
import tornado.ioloop
from tornado.escape import json_decode
import json
import os 
import pymysql as torndb

connect = torndb.connect('192.168.15.39',user='test',password='test',db='test')
cursor = connect.cursor()
connect.autocommit(True)
import nginxparser

class WebApiHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        data=json_decode(self.request.body)
        print(data)
        k,v = data.popitem()
        v = json.dumps(v)
        cursor.execute("insert into proxy_info(ip,backstage) VALUES (%s,%s) on DUPLICATE key update backstage=VALUES(backstage)",(k,v))
        '''
        for d in jdata:
            port = d['port']
            remote_ip = d['ip']
            remote_ip = ','.join(remote_ip)
            upstream_name = d['upstream']
        '''

class WebInfoHandler(tornado.web.RequestHandler):
    def get(self):

        data = {}
        cursor.execute("select * from proxy_info;")
        res = cursor.fetchall()
        for info in res:
            k,v = info[0],info[1]
            data[k] = json_decode(v)

        self.render(r'web\diagram\nginx.html', data=data)

class DockerApiHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        data=json_decode(self.request.body)
        print(type(data))
        #cursor.execute("insert into proxy_info(ip,backstage) VALUES (%s,%s) on DUPLICATE key update backstage=VALUES(backstage)",(k,v))



if __name__ == "__main__":
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__),'templates'),
        'static_path': os.path.join(os.path.dirname(__file__),'static')
    }
    app = tornado.web.Application([
        (r'/api/web', WebApiHandler),
        (r'/api/docker', DockerApiHandler),
        (r'/web/info', WebInfoHandler)
    ], **settings)
    app.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
