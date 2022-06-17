import tornado.web
import tornado.escape
from urllib.parse import unquote
import requests
import random
import os

from core.database import(
    SessionLocal,
    engine,
    Base,
    get_db
)
from handler.login import(
    login
)

from model.title import(
    Title,
    TitleType,
    TitleData
)
from model.user import User

from handler.dashboard.dashboard import(
    index,
    title_add,
    title_list,
    api_title_type_list,
    api_title_special_key_from,
    api_title_add,
    api_data_from_id,
    api_next,
    api_data,
    api_title_list,
    title_edit,
    api_load_data_from_video,
    api_title_update,
    api_title_add_source,
    api_title_add_subtitle,
    title_edit_content,
    api_title_add_inside,
    download_list,
    #download_upload
)
from handler.base import(
    baseAuthenticated,
    baseAuthenticatedAPI
)

from source.uptobox import uptobox


Base.metadata.create_all(bind=engine)




class MainHandler2(tornado.web.RequestHandler):
    def initialize(self, db_inst):
        self.db_inst = db_inst
    def get(self):
        a = Title.add(self.db_inst, 'aaa', 1)
        self.write('q')



def download_from_uptobox(url):
    response_premium = uptobox(url, cookie)
    if response_premium.status_code == 302:
        url_premium = response_premium.headers['location']
        name = url_premium[url_premium.rindex('/')+1:]
        if os.path.isfile(name) == False:
            r = requests.get(url_premium, allow_redirects=True)
            with open(name, 'wb') as f:
                f.write(r.content)
            return name
        else:
            return name
    else:
        return False




def body_handler(data):
    data = data.decode()
    temp = {}
    for item in data.split('&'):
        key = item.split('=')[0].strip()
        value = unquote(item.split('=')[1].strip())
        temp.update({key: value})
    return temp



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie("mycookie"):
            self.write("""<!doctype html><html><body><form method="POST"><input type="text" name="key"><input type="submit" value="ok"></form></body></html>""")
        else:
            cookie = self.get_cookie('mycookie')
            if cookie == 'MzAwNQ==':
                for arquivo in arquivos:
                    self.write(f'<a href="/assistir?id={arquivo["key"]}">{arquivo["titulo"]}</a><br />')
            else:
                self.write('nope')
    def post(self):
        data = body_handler(self.request.body)
        print(data)
        if data.get('key', '0') == 'MzAwNQ==':
            self.set_cookie("mycookie", "MzAwNQ==")
            self.redirect('/')
        else:
            self.write('nope')



class Assistir(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('id', False)
        if id != False:
            ver_id = False
            for item in arquivos:
                if item['key'] == id:
                    ver_id = item
                    break
            if ver_id != False:
                response_url = uptobox(ver_id['url'], cookie)
                if response_url.status_code == 302:
                    url_request = response_url.headers['location']
                    self.write(f'{ver_id["titulo"]}<br /><br />')
                    self.write(f'<video width="400" controls><source src="{url_request}" type="video/mp4">')
                    if 'sub' in ver_id:
                        response_url_sub = uptobox(ver_id['sub'], cookie)
                        if response_url_sub.status_code == 302:
                            self.write(f'<track src="/subtitle?id={ver_id["key"]}"" kind="subtitles" srclang="en" label="English">')
                    self.write('Your browser does not support HTML video.</video>')
                else:
                    self.write('erro gerar link')
            else:
                self.write('id invalido')
        else:
            self.write('sem id')


def convert_srt2vtt(data):
    data = data.decode('latin-1').encode('utf-8').decode('utf-8')
    data_s = data.split('\n\n')
    output = 'WEBVTT\n\n'
    for item in data_s:
        item_s = item.split('\n')
        first = True
        for item2 in item_s[1:]:
            if first:
                first = False
                pass
            if '-->' in item2:
                item2 = item2.replace(',', '.')
            output += item2 + '\n'
        output += '\n'
    return output



class vtt(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('url', False)
        if id != False:
            temp = requests.get(id)
            print(temp.encoding)
            if id.endswith('.srt'):
                output = convert_srt2vtt(temp.content)
            else:
                output = temp.text
            self.set_header('content-type', 'text/vtt; charset=UTF-8')
            self.write(output)
        else:
            self.write('sem id')


class dash(tornado.web.RequestHandler):
    def get(self):
        self.render('view/dashboard/content.html')


class watch(baseAuthenticated):
    def get(self):
        id_from = self.get_argument('id_from', False)
        if id_from == False:
            titulos = Title.find_by_type_id_in(self.db, (1, 2))
        else:
            titulos = Title.find_by_id_title_belong(self.db, id_from)
        for i in titulos:
            if i['id_title_type'] in (1, 4):
                self.write(f'<a href="/video?id={i["id"]}">{i["description"]}</a><br />')
            else:
                self.write(f'<a href="/assistir?id_from={i["id"]}">{i["description"]}</a><br />')


class video(baseAuthenticated):
    def get(self):
        id = self.get_argument('id', False)
        if id != False:
            data_title = TitleData.find_by_title_id(self.db, id_title=id)
            # data_source = [
            #     {
            #         'source': uptobox('https://uptobox.com/g6iknjxcfyir').headers['location'],
            #         'quality': '720p'
            #     },
            #     {
            #         'source': uptobox('https://uptobox.com/sme7cwks4m6m').headers['location'],
            #         'quality': '480p'
            #     }
            # ]
            self.render('view/video.html', video_id = id)

def make_app():
    return tornado.web.Application(
        [
            (r"/", login, dict(db_inst=SessionLocal())),
            (r"/assistir", watch, dict(db_inst=SessionLocal())),
            (r"/subtitle", vtt),
            (r"/aa", MainHandler2, dict(db_inst=SessionLocal())),
            (r"/dashboard", index, dict(db_inst=SessionLocal())),
            (r"/dashboard/titulo/adicionar", title_add, dict(db_inst=SessionLocal())),
            (r"/dashboard/titulo/listar", title_list, dict(db_inst=SessionLocal())),
            (r"/dashboard/download/listar", download_list, dict(db_inst=SessionLocal())),
            # (r"/dashboard/download/upload", download_upload, dict(db_inst=SessionLocal())),
            (r"/dashboard/titulo/editar", title_edit, dict(db_inst=SessionLocal())),
            (r"/dashboard/titulo/editar-conteudo", title_edit_content, dict(db_inst=SessionLocal())),
            (r"/api/next-video", api_next, dict(db_inst=SessionLocal())),
            (r"/api/dashboard/titulo/list-title-types", api_title_type_list, dict(db_inst=SessionLocal())),
            (r"/api/dashboard/titulo/list-title-special-key", api_title_special_key_from, dict(db_inst=SessionLocal())),
            (r"/api/dashboard/titulo/add", api_title_add, dict(db_inst=SessionLocal())),
            (r"/api/dashboard/titulo/add-inside", api_title_add_inside, dict(db_inst=SessionLocal())),
            (r"/api/video-data", api_data_from_id, dict(db_inst=SessionLocal())),
            (r"/api/add-video-data", api_title_add_source, dict(db_inst=SessionLocal())),
            (r"/api/add-video-subtitle", api_title_add_subtitle, dict(db_inst=SessionLocal())),
            (r"/api/title-list", api_title_list, dict(db_inst=SessionLocal())),
            (r"/api/title-detail", api_load_data_from_video, dict(db_inst=SessionLocal())),
            (r"/api/detail-video", api_data, dict(db_inst=SessionLocal())),
            (r"/api/update-detail-title", api_title_update, dict(db_inst=SessionLocal())),
            (r'/dashboard/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/dashboard'}),
            (r'/video', video, dict(db_inst=SessionLocal()))
            # (r"/list-all", shoplist_list_all, dict(db_inst=db_inst)),
            # (r"/list/(.*)", shoplist_list, dict(db_inst=db_inst)),
            # (r"/api/list/create", shoplist_create_api, dict(db_inst=db_inst)),
            # (r"/api/list/(.*)/add", shoplist_list_add_api, dict(db_inst=db_inst)),
            # (r"/api/list/(.*)/edit/(.*)", shoplist_list_edit_api, dict(db_inst=db_inst)),
            # (r"/api/list/(.*)/delete/(.*)", shoplist_list_delete_api, dict(db_inst=db_inst)),
            # (r"/api/list/(.*)", shoplist_list_api, dict(db_inst=db_inst)),
            # (r"/api/list-all", shoplist_list_all_api, dict(db_inst=db_inst)),
            # (r"/main-functions.js", shoplist_js),
        ], 
        settings = {
            "template_path": 'view/'
        },
        cookie_secret="abcdefghjue82378129393",
        debug=True
    )



port_http_server = 8886


if __name__ == "__main__":
    app = make_app()
    app.listen(port_http_server)
    tornado.ioloop.IOLoop.current().start()


