import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.web
import threading
import time
import os

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")
class MyWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = dict()
    def open(self, *args):
        self.id = self.get_argument("id")
        self.stream.set_nodelay(True)
        self.clients[self.id] = {"id": self.id, "object": self}
        print(self.id,self.clients)
    def on_message(self, message):
        print("clinet %s receive a message: %s" % (self.id,message))
        self.sendTime()

    def sendTime(self):
        import datetime
        while True:
            for key in self.clients.keys():
                msg = str(datetime.datetime.now())
                self.clients[key]["object"].write_message(msg)
                print("write to client %s" % key)
            time.sleep(1)

    def on_close(self):
        if self.id in self.clients:
            del self.clients[self.id]
            print("client %s is closed" % self.id)
    def check_origin(self, origin):
        return True

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/websocket', MyWebSocketHandler),
],**{
    "template_path": os.path.join(os.path.dirname(__file__),"templates")
}
)




if __name__ == "__main__":
    app.listen(9000)
    tornado.ioloop.IOLoop.instance().start()

