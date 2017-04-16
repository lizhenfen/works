#!/usr/bin/python

import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options, parse_command_line

define('port', default=8080, help='run on the given port', type=int)
'''
    1. 用户填写记录，发送到后台
    2. 后台接收信息，并保存到数据库
    3. 页面上显示记录
    4. 可修改页面

'''
class NginxIndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
    def post(self):
        nginx_user = self.get_arguments('nginx_user')
        worker_connections = self.get_arguments('worker_connections')
        worker_rlimit_nofile = self.get_arguments('worker_rlimit_nofile')
        server_tokens = self.get_arguments('server_tokens')
        network_control = self.get_arguments('network_control')
        net_push = self.get_arguments('net_push')
        keepalive_timeout = self.get_arguments('keepalive_timeout')
        gzip_switch = self.get_arguments('gzip_switch')
        gzip_min_length = self.get_arguments('gzip_min_length')
        nginx = {
            'nginx_user': 'nginx',
            'worker_connections': 10240,
            'worker_rlimit_nofile': 10240,
            'server_tokens': 'off',
            'network_control': 'on',
            'net_push':'on',
            'keepalive_timeout': 75,
            'gzip_switch': 'on',
            'gzip_min_length': 1000,
        }
        
        #self.render('nginx.yaml', **nginx)
        self.redirect('/')
        
class NginxUpstreamHandler(tornado.web.RequestHandler):
    def post(self): 
        upstream = {
            'name': 'test',
            'port': 443,
            'ips': [{
                'ip': '10.0.0.1',
                'weight': 10,
                'count': 2,
                'timeout': 2,
                },],
            'server_name': 'test.vats.com.cn',
            'ssl': True,
            'log_swith': True
        }
        self.render('upstream.yaml', upstream=upstream)
        

def make_app():
    return tornado.web.Application([
        (r'/', NginxIndexHandler),
        (r'/xxx', NginxUpstreamHandler)
    ])
        
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
        
