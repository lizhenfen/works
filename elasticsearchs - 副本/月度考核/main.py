import tornado.web
import tornado.ioloop
import tornado.httpserver

from urls import uri
from conf import settings


class App(tornado.web.Application):
    def __init__(self):
        super(App,self).__init__(uri,**settings.settings)

if __name__ == "__main__":
    app = App()
    httpserver = tornado.httpserver.HTTPServer(app)
    #httpserver.listen(settings.port)
    httpserver.listen(9003)
    tornado.ioloop.IOLoop.instance().start()