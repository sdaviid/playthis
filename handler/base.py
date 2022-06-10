import tornado.web
import os
from urllib.parse import unquote

class baseAuthenticated(tornado.web.RequestHandler):
    def initialize(self, db_inst):
        self.db = db_inst
    def render_base(self, path, **kwg):
        path_final = '../{}'.format(path if not path.startswith('/') else path[1:])
        print(path_final)
        self.render(path_final, **kwg)
    def prepare(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        if not self.get_cookie("mycookie"):
            self.redirect('/')
    def body_handler(self):
        data = self.request.body.decode('utf-8')
        temp = {}
        for item in data.split('&'):
            key = item.split('=')[0].strip()
            value = unquote(item.split('=')[1].strip())
            temp.update({key: value})
        return temp



class baseAuthenticatedAPI(baseAuthenticated):
    def prepare(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header('content-type', 'application/json')
        if not self.get_cookie("mycookie"):
            self.redirect('/')