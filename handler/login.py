import tornado.web
from model.user import User
from model.title import Title
from urllib.parse import unquote



def body_handler(data):
    data = data.decode()
    temp = {}
    for item in data.split('&'):
        key = item.split('=')[0].strip()
        value = unquote(item.split('=')[1].strip())
        temp.update({key: value})
    return temp



class login(tornado.web.RequestHandler):
    def initialize(self, db_inst):
        self.db = db_inst
    def get(self):
        if not self.get_cookie("mycookie"):
            self.render('../view/login.html')
        else:
            cookie = self.get_cookie('mycookie')
            if cookie == 'MzAwNQ==':
                self.redirect('/assistir')
            else:
                self.write('nope')
    def post(self):
        data = body_handler(self.request.body)
        username = data.get('username', False)
        password = data.get('password', False)
        if username != False and password != False:
            data_check = User.make_login(session=self.db, user=username, password=password)
            if data_check:
                self.set_cookie("mycookie", "MzAwNQ==")
                self.redirect('/')
            else:
                self.write('nope')
        else:
            self.write('nope')