#tornado 实现代理
# -*- coding: utf-8 -*-
#
# Copyright(c) 2011 Felinx Lee &amp; http://feilong.me/
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado.web import HTTPError, asynchronous
from tornado.httpclient import HTTPRequest
from tornado.options import define, options
try:
    from tornado.curl_httpclient import CurlAsyncHTTPClient as AsyncHTTPClient
except ImportError:
    from tornado.simple_httpclient import SimpleAsyncHTTPClient as AsyncHTTPClient

define("port", default=8888, help="run on the given port", type=int)
define("api_protocol", default="http")
define("api_host", default="feilong.me")
define("api_port", default="80")
define("debug", default=True, type=bool)

class ProxyHandler(tornado.web.RequestHandler):
    @asynchronous
    def get(self):
        # enable API GET request when debugging
        if options.debug:
            return self.post()
        else:
            raise HTTPError(405)

    @asynchronous
    def post(self):
        protocol = options.api_protocol
        host = options.api_host
        port = options.api_port

        # port suffix
        port = "" if port == "80" else ":%s" % port

        uri = self.request.uri
        url = "%s://%s%s%s" % (protocol, host, port, uri)

        # update host to destination host
        headers = dict(self.request.headers)
        headers["Host"] = host

        try:
            AsyncHTTPClient().fetch(
                HTTPRequest(url=url,
                            method="POST",
                            body=self.request.body,
                            headers=headers,
                            follow_redirects=False),
                self._on_proxy)
        except tornado.httpclient.HTTPError, x:
            if hasattr(x, "response") and x.response:
                self._on_proxy(x.response)
            else:
                logging.error("Tornado signalled HTTPError %s", x)

    def _on_proxy(self, response):
        if response.error and not isinstance(response.error,
                                             tornado.httpclient.HTTPError):
            raise HTTPError(500)
        else:
            self.set_status(response.code)
            for header in ("Date", "Cache-Control", "Server", "Content-Type", "Location"):
                v = response.headers.get(header)
                if v:
                    self.set_header(header, v)
            if response.body:
                self.write(response.body)
            self.finish()

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/.*", ProxyHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()