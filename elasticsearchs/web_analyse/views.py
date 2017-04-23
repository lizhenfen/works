import tornado.web

class MainHandler(tornado.web.RequestHandler):
    pass

class IndexHandler(MainHandler):
    def get(self):
        self.render("base.html")

class CollectHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        data = self.get_argument("data")
        print(data)

class DataReportHandler(tornado.web.RequestHandler):
    pass