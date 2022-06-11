from handler.base import(
    baseAuthenticated,
    baseAuthenticatedAPI
)
from model.title import(
    Title,
    TitleType,
    TitleData,
    TitleDataSubtitle
)
from model.data import DataSource
from source.uptobox import uptobox
import json


class api_title_type_list(baseAuthenticatedAPI):
    def get(self):
        default_body = {'status': False}
        data = TitleType.list_all(self.db)
        if data:
            default_body.update({'status': True, 'data': []})
            for item in data:
                temp = {
                    'id': item.id,
                    'description': item.description,
                    'key': item.key,
                    'date_created': item.date_created
                }
                default_body['data'].append(temp)
        self.write(json.dumps(default_body, default=str))


class api_title_special_key_from(baseAuthenticatedAPI):
    def get(self):
        default_body = {'status': False}
        title_type_id = self.get_argument('id_type', False)
        if title_type_id != False:
            data = Title.find_by_type_id(self.db, title_type_id)
            if data:
                default_body.update({'status': True, 'data': []})
                for item in data:
                    temp = {
                        'id': item.id,
                        'description': item.description,
                        'id_title': item.id_title,
                        'id_title_type': item.id_title_type,
                        'date_created': item.date_created
                    }
                    default_body['data'].append(temp)
        self.write(json.dumps(default_body, default=str))


class api_next(baseAuthenticatedAPI):
    def get(self):
        id_base = self.get_argument('id')
        title_running = Title.find_by_id(self.db, id_base)
        title_father_running = Title.find_by_id(self.db, title_running[0].id_title)
        print(title_father_running)
        title_father = Title.find_by_id_father(self.db, title_father_running[0].id_title)
        title_father_id = []
        for item in title_father:
            title_father_id.append(item.id)
        print(title_father_id)
        titles_from_father = Title.find_by_id_father_in(self.db, title_father_id)
        response = []
        for item in titles_from_father:
            if item.id > int(id_base):
                response.append({
                    'id': item.id,
                    'description': item.description
                })
        self.write(json.dumps(response))


class api_data(baseAuthenticatedAPI):
    def get(self):
        default_body = {'status': False}
        id_base = self.get_argument('id')
        title = Title.find_by_id(self.db, id_base)
        if title:
            default_body.update({'status': True, 'title': title[0].description})
        self.write(default_body)



class api_title_list(baseAuthenticatedAPI):
    def get(self):
        default_body = {'status': False}
        id_from = self.get_argument('id_from', False)
        if id_from == False or id_from == '0':
            titulos = Title.find_by_type_id_in(self.db, (1, 2))
        else:
            titulos = Title.find_by_id_title_belong(self.db, id_from)
        if titulos:
            default_body.update({'status': True, 'data': []})
            for item in titulos:
                temp_source = []
                temp_subtitle = []
                title_data = TitleData.find_by_title_id(self.db, item.id)
                title_data_subtitle = TitleDataSubtitle.find_by_title_id(self.db, item.id)
                if title_data:
                    for item_source in title_data:
                        print(item_source.data)
                        print(temp_source)
                        temp_data_source = {
                            'id': item_source.id,
                            'id_title': item_source.id_title,
                            'id_data_source': item_source.id_data_source,
                            'data': item_source.data,
                            'language': item_source.language,
                            'quality': item_source.quality
                        }
                        temp_source.append(temp_data_source)
                if title_data_subtitle:
                    for item_source_subtitle in title_data_subtitle:
                        temp_data_subtitle = {
                            'id': item_source_subtitle.id,
                            'id_title': item_source_subtitle.id_title,
                            'id_data_source': item_source_subtitle.id_data_source,
                            'data': item_source_subtitle.data,
                            'language': item_source_subtitle.language
                        }
                        temp_subtitle.append(temp_data_subtitle)
                temp = {
                    'id': item.id,
                    'description': item.description,
                    'id_title_type': item.id_title_type,
                    'source': temp_source,
                    'subtitle': temp_subtitle
                }
                default_body['data'].append(temp)
        self.write(default_body)



class api_load_data_from_video(baseAuthenticatedAPI):
    def get(self):
        default_body = {'status': False}
        id = self.get_argument('id', False)
        if id != False:
            data_title = Title.find_by_id(self.db, id=id)
            if data_title:
                default_body.update({'status': True, 'data': {}})
                default_body['data'].update({
                    'id': id,
                    'description': data_title[0].description,
                    'id_title': data_title[0].id_title,
                    'id_title_type': data_title[0].id_title_type,
                    'date_created': data_title[0].date_created
                })
                data_title_data = TitleData.find_by_title_id(self.db, id_title=id)
                data_title_subtitle = TitleDataSubtitle.find_by_title_id(self.db, id_title=id)
                if data_title_data:
                    default_body['data'].update({'source': []})
                    for item in data_title_data:
                        temp = {
                            'id': item.id,
                            'id_title': item.id_title,
                            'id_data_source': item.id_data_source,
                            'data': item.data,
                            'language': item.language,
                            'quality': item.quality,
                            'date_created': item.date_created
                        }
                        default_body['data']['source'].append(temp)
                if data_title_subtitle:
                    default_body['data'].update({'subtitle': []})
                    for item in data_title_subtitle:
                        temp = {
                            'id': item.id,
                            'id_title': item.id_title,
                            'id_data_source': item.id_data_source,
                            'data': item.data,
                            'language': item.language,
                            'date_created': item.date_created
                        }
                        default_body['data']['subtitle'].append(temp)
        self.write(json.dumps(default_body, default=str))




class api_data_from_id(baseAuthenticatedAPI):
    def get(self):
        default_body = {'status': False}
        id_title = self.get_argument('id', False)
        if id_title != False:
            data_title = TitleData.find_by_title_id(self.db, id_title=id_title)
            data_title_subtitle = TitleDataSubtitle.find_by_title_id(self.db, id_title=id_title)
            data_source = []
            data_subtitle = []
            for item in data_title:
                print(item['id_data_source'])
                if str(item['id_data_source']) == '1':
                    print('kkkkk tem que rir pae')
                    data = uptobox(item['data'])
                else:
                    data = item['data']
                temp = {
                    'id': item['id'],
                    'id_title': item['id_title'],
                    'id_data_source': item['id_data_source'],
                    'data': data,
                    'language': item['language'],
                    'quality': item['quality'],
                    'date_created': item['date_created']
                }
                data_source.append(temp)
            for item in data_title_subtitle:
                if str(item['id_data_source']) == '1':
                    data = uptobox(item['data'])
                else:
                    data = item['data']
                temp = {
                    'id': item['id'],
                    'id_title': item['id_title'],
                    'id_data_source': item['id_data_source'],
                    'data': data,
                    'language': item['language'],
                    'date_created': item['date_created']
                }
                data_subtitle.append(temp)
            data_output = {
                'source': data_source,
                'subtitle': data_subtitle
            }
            default_body = {'status': True, 'data': data_output}
            print(data_output)
            self.write(json.dumps(default_body, default=str))


class api_title_update(baseAuthenticatedAPI):
    def post(self):
        default_body = {'status': False}
        id = self.get_argument('id', False)
        data_body = self.body_handler()
        if id and data_body:
            title_name = data_body.get('title-name', False)
            title_type = data_body.get('sel-type-title', False)
            title_belong = data_body.get('sel-title-belong', None)
            if title_name and title_type:
                data = Title.update(self.db, id=id, description=title_name, id_title=title_belong, id_title_type=title_type)
                if data:
                    default_body.update({'status': True, 'data': {'id': data.id, 'description': data.description, 'id_title': data.id_title, 'id_title_type': data.id_title_type, 'date_created': data.date_created}})
        self.write(json.dumps(default_body, default=str))



class api_title_add_source(baseAuthenticatedAPI):
    def post(self):
        default_body = {'status': False}
        id = self.get_argument('id', False)
        data_body = self.body_handler()
        if id and data_body:
            data_source = data_body.get('data-content', False)
            type_source = data_body.get('type-source', False)
            language = data_body.get('language', False)
            quality = data_body.get('quality', False)
            data_new = TitleData.add(self.db, id_title=id, id_data_source=type_source, data=data_source, language=language, quality=quality)
            if data_new:
                default_body.update({'status': True, 'data': {'id': data_new.id, 'id_title': data_new.id_title, 'id_data_source': data_new.id_data_source, 'data': data_new.data, 'language': data_new.language, 'quality': data_new.quality}})
        self.write(json.dumps(default_body, default=str))



class api_title_add_subtitle(baseAuthenticatedAPI):
    def post(self):
        default_body = {'status': False}
        id = self.get_argument('id', False)
        data_body = self.body_handler()
        if id and data_body:
            data_source = data_body.get('data-content', False)
            type_source = data_body.get('type-source', False)
            language = data_body.get('language', False)
            data_new = TitleDataSubtitle.add(self.db, id_title=id, id_data_source=type_source, data=data_source, language=language)
            if data_new:
                default_body.update({'status': True, 'data': {'id': data_new.id, 'id_title': data_new.id_title, 'id_data_source': data_new.id_data_source, 'data': data_new.data, 'language': data_new.language}})
        self.write(json.dumps(default_body, default=str))



class api_title_add_inside(baseAuthenticatedAPI):
    def post(self):
        default_body = {'status': False}
        data_body = self.body_handler()
        if data_body != False:
            title_name = data_body.get('title-name', False)
            title_type = data_body.get('sel-type-title', False)
            title_belong = data_body.get('sel-title-belong', None)
            data_source = json.loads(json.dumps(data_body.get('source', [])))
            data_subtitle = json.loads(json.dumps(data_body.get('subtitle', [])))
            if title_name != False and title_type != False:
                data_new_title_episode = Title.add(self.db, description=title_name, id_title=title_belong, id_title_type=4)
                if data_new_title_episode:
                    default_body.update({'status': True, 'data': {'id': data_new_title_episode.id, 'description': data_new_title_episode.description, 'id_title': data_new_title_episode.id_title, 'id_title_type': data_new_title_episode.id_title_type, 'date_created': data_new_title_episode.date_created, 'source': [], 'subtitle': []}})
                    for item in json.loads(data_source):
                        print(item)
                        temp_new_source = TitleData.add(self.db, id_title=data_new_title_episode.id, id_data_source=1, data=item['data'], language=item['language'], quality=item['quality'])
                        if temp_new_source:
                            default_body['data']['source'].append({
                                'id': temp_new_source.id,
                                'id_title': temp_new_source.id_title,
                                'id_data_source': temp_new_source.id_data_source,
                                'data': temp_new_source.data,
                                'language': temp_new_source.language,
                                'quality': temp_new_source.quality,
                                'date_created': temp_new_source.date_created
                            })
                    for item_subtitle in json.loads(data_subtitle):
                        temp_new_subtitle = TitleDataSubtitle.add(self.db, id_title=data_new_title_episode.id, id_data_source=1, data=item_subtitle['data'], language=item_subtitle['language'])
                        if temp_new_subtitle:
                            default_body['data']['subtitle'].append({
                                'id': temp_new_subtitle.id,
                                'id_title': temp_new_subtitle.id_title,
                                'id_data_source': temp_new_subtitle.id_data_source,
                                'data': temp_new_subtitle.data,
                                'language': temp_new_subtitle.language,
                                'date_created': temp_new_subtitle.date_created
                            })
        self.write(json.dumps(default_body, default=str))


class api_title_add(baseAuthenticatedAPI):
    def post(self):
        default_body = {'status': False}
        data_body = self.body_handler()
        if data_body != False:
            title_name = data_body.get('title-name', False)
            title_type = data_body.get('sel-type-title', False)
            title_belong = data_body.get('sel-title-belong', None)
            data_source = json.loads(json.dumps(data_body.get('data-source', [])))
            data_subtitle = json.loads(json.dumps(data_body.get('subtitle', [])))
            if title_name != False and title_type != False:
                data_new_title = Title.add(self.db, description=title_name, id_title=title_belong, id_title_type=title_type);
                if data_new_title:
                    default_body.update({'status': True, 'data': {'id': data_new_title.id, 'description': data_new_title.description, 'id_title': data_new_title.id_title, 'id_title_type': data_new_title.id_title_type, 'date_created': data_new_title.date_created, 'title': []}});
                    if data_source:
                        for data_item in json.loads(data_source):
                            sources = []
                            subtitles = []
                            data_new_title_episode = Title.add(self.db, description=data_item['title'], id_title=data_new_title.id, id_title_type=4)
                            for data_item_source in data_item['source']:
                                data_new_source = TitleData.add(self.db, id_title=data_new_title_episode.id, id_data_source=1, data=data_item_source['source'], language=data_item_source['language'], quality=data_item_source['quality'])
                                if data_new_source:
                                    sources.append({'id': data_new_source.id, 'id_title': data_new_source.id_title, 'id_data_source': data_new_source.id_data_source, 'data': data_new_source.data, 'language': data_new_source.language, 'quality': data_new_source.quality})
                            for data_item_subtitle in data_item["subtitle"]:
                                data_new_subtitle = TitleDataSubtitle.add(self.db, id_title=data_new_title_episode.id, id_data_source=1, data=data_item_subtitle['source'], language=data_item_subtitle['language'])
                                if data_new_subtitle:
                                    subtitles.append({'id': data_new_subtitle.id, 'id_title': data_new_subtitle.id_title, 'id_data_source': data_new_subtitle.id_data_source, 'data': data_new_subtitle.data, 'language': data_new_subtitle.language})
                            default_body['data']['title'].append({'id': data_new_title_episode.id, 'description': data_new_title_episode.description, 'id_title': data_new_title_episode.id_title, 'id_title_type': data_new_title_episode.id_title_type, 'source': sources, 'subtitle': subtitles, 'date_created': data_new_title_episode.date_created})
                else:
                    default_body.update({'message': 'error adding new title'});
        self.write(json.dumps(default_body, default=str))






class index(baseAuthenticated):
    def get(self):
        self.render_base('view/dashboard/content.html')


class title_add(baseAuthenticated):
    def get(self):
        self.render_base('view/dashboard/titulo-adicionar.html')



class title_list(baseAuthenticated):
    def get(self):
        id_from = self.get_argument('id_from', 0)
        self.render_base('view/dashboard/titulo-listar.html', **{'id_from': id_from})



class title_edit(baseAuthenticated):
    def get(self):
        id_from = self.get_argument('id_from', False)
        if id_from != False:
            self.render_base('view/dashboard/titulo-editar.html', **{'id_from': id_from})


class title_edit_content(baseAuthenticated):
    def get(self):
        id_from = self.get_argument('id_from', False)
        if id_from != False:
            self.render_base('view/dashboard/titulo-editar-conteudo.html', **{'id_from': id_from})