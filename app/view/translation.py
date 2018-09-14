from tornado.web import HTTPError
from app.dal import translation
from app.dal import languages
from app.dal import application
from app.dal import character
from app.tools import tool
import tornado.web
import json
import math
from app.view.basehandler import BaseHandler


class TranslationHandler(BaseHandler):
    def get(self,translation_id = ''):   #list和指定id查询
        header = self._headers
        print(type(header))
        if translation_id == '':
            respon_json = translation.db_get_translation_list()
        else:
            respon_json = translation.db_get_translation_id(translation_id)
        respon_json = json.dumps(respon_json)
        self.write(respon_json)



    def post(self, *args, **kwargs):#增加

        param_list = self.request.body.decode('utf-8')
        param_list = json.loads(param_list)
        for param in param_list:
            argu_keys = param.keys()
            if 'language_id' not in argu_keys or 'application_id' not in argu_keys or 'character_id' not in argu_keys or \
                            'cha_translation' not in argu_keys:  # 判断键是否正确
                raise HTTPError(400, reason="KeyError", log_message="key not exist")
        for param in param_list:
            language_id = param['language_id']
            application_id = param['application_id']
            character_id = param['character_id']
            cha_translation = param['cha_translation']
            if application_id == 0:
                application_id = None
            post_flag = translation.db_get_id_translation(language_id,application_id, character_id)
            if post_flag:
                raise HTTPError(400, reason="InsertDataError", log_message="data exist")

        response = translation.db_insert_translation(param_list)
        respon_json = []
        for i in response:
            response = tool.translation2dict(i)
            respon_json.append(response)
        respon_json = json.dumps(respon_json)
        self.write(respon_json)

    def delete(self, translation_id = None):#删除
        if translation_id is None:
            raise HTTPError(405)
        param = self.request.body.decode('utf-8')
        prarm = json.loads(param)
        language_id = prarm['language_id']
        application_id = prarm['application_id']
        character_id = prarm['character_id']
        if application_id == 0:
            application_id = None
        delete_flag = translation.db_get_id_translation(language_id, application_id, character_id)
        if delete_flag:
            delete_data = translation.db_delete_translation(language_id, application_id, character_id)
            respon_json = json.dumps(delete_flag)
            self.write(respon_json)
        else:
            raise HTTPError(400, reason="FoundDataError", log_message="not found data")


    #根据app_id,lan_id,cha_id进行更新
    def put(self,translation_id = None): #
        if translation_id is None:
            raise HTTPError(405)
        param = self.request.body.decode('utf-8')
        prarm = json.loads(param)
        argu_keys = prarm.keys()
        if 'language_id' in argu_keys and 'application_id' in argu_keys and 'character_id' in argu_keys and \
                'cha_translation' in argu_keys: #判断键是否正确
            language_id = prarm['language_id']
            application_id = prarm['application_id']
            character_id = prarm['character_id']
            cha_translation = prarm['cha_translation']
            if application_id == 0:
                application_id = None
            put_data = translation.db_get_id_translation(language_id, application_id, character_id)
            if put_data:
                response = translation.db_update_translation(language_id, application_id, character_id,cha_translation)
                response = tool.translation2dict(response)
                respon_json = json.dumps(response)
                self.write(respon_json)
            else:
                raise HTTPError(400, reason="FoundDataError", log_message="not found data")
        else:
            raise HTTPError(400, reason="KeyError", log_message="key not exist")

    def write_error(self,status_code, **kwargs):
        exc_info = kwargs.get("exc_info", None)
        exc = exc_info[1]
        if isinstance(exc, HTTPError):
            rsp = {
                "RequestId": 'a',
                "Error":{
                    "Code": exc.reason,
                    "Message": exc.log_message,
                    "Type": "Response"
                }
            }
            self.write(rsp)
            self.finish()

    def patch(self, *args, **kwargs):
        raise HTTPError(405)


class TranslationPageHandler(BaseHandler):

    def get(self, *args, **kwargs):
        respon_json = []
        page_size = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        query,count = translation.db_get_translation_page(page_size,page)
        for i in query:
            json_transform = tool.translation2dict(i)
            respon_json.append(json_transform)
        data_count = count
        current_number = page
        page_count = math.ceil(count/int(page_size))
        respon_json = tool.pageResponse(data_count,int(current_number),page_count,int(page_size),respon_json)
        respon_json = json.dumps(respon_json)
        self.write(respon_json)

    def write_error(self,status_code, **kwargs):
        exc_info = kwargs.get("exc_info", None)
        exc = exc_info[1]
        if isinstance(exc, HTTPError):
            rsp = {
                "RequestId": 'a',
                "Error":{
                    "Code": exc.reason,
                    "Message": exc.log_message,
                    "Type": "Response"
                }
            }
            self.write(rsp)
            self.finish()



class MultiHandler(BaseHandler):
    def get(self,app_public = '',app = ''):
        """
        获取某language，某application翻译
        :param app_public:
        :param app: 项目
        :return:
        """
        accept_language = self.get_argument('lang',None)
        if accept_language == None:
            headers = self.request.headers
            accept_language = headers['Accept-Language']
            query = languages.db_get_id_language(accept_language)

        else:
            query = languages.db_get_id_language(accept_language)
        if query == {}:
            public_list = {}
        else:
            language_id = query['id']
            query_app = application.db_get_id_application(app)
            if query_app == {}:
                raise HTTPError(400, reason="AppError", log_message="app not exist")
            else:
                application_id = query_app['id']
                translation_list = translation.db_get_language_translation(language_id, application_id)
                public_list = translation.db_get_language_translation(language_id, None)
                public_list.update(translation_list)
        respon_json = json.dumps(public_list)
        self.write(respon_json)

    def write_error(self, status_code, **kwargs):
        exc_info = kwargs.get("exc_info", None)
        exc = exc_info[1]
        if isinstance(exc, HTTPError):
            rsp = {
                "RequestId": 'a',
                "Error": {
                    "Code": exc.reason,
                    "Message": exc.log_message,
                    "Type": "Response"
                }
            }
            self.write(rsp)
            self.finish()


class PublicHandler(BaseHandler):
    """
    获取公共部分翻译
    """
    def get(self):
        """
        :return: 某语言下公共部分数据,translation表中application_id=none未公共部分
        """
        accept_language = self.get_argument('lang',None)
        if accept_language == None:
            headers = self.request.headers
            accept_language = headers['Accept-Language']
            query = languages.db_get_id_language(accept_language)
        else:
            query = languages.db_get_id_language(accept_language)
        if query == {}:
            result = {}
        else:
            language_id = query['id']
            result = translation.db_get_language_translation(language_id, None)
        respon_json = json.dumps(result)
        self.write(respon_json)



class NewTransHandler(BaseHandler):

    def get(self, *args, **kwargs):
        respon_json = []
        page_size = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        app = self.get_argument('app', 'all')
        if app == 'all':
            app_id = 0
            query,count = translation.db_get_translation_group(page_size,page,app_id)
            for i in query:
                character_id = i[0]
                application_id = i[1]
                language_list = translation.db_get_translation_cha_id_app_id(character_id,application_id)
                character_msg = character.db_get_character_id(character_id)
                application_msg = application.db_get_application_id(application_id)
                json_transform = tool.newGet(character_msg,application_msg)
                respon_json.append(json_transform)
            data_count = count
            current_number = page
            page_count = math.ceil(count/int(page_size))
            respon_json = tool.pageResponse(data_count,int(current_number),page_count,int(page_size),respon_json)
            respon_json = json.dumps(respon_json)
        elif app == 'public':
            app_id = None
            query,count = translation.db_get_translation_group(page_size,page,app_id)
            for i in query:
                character_id = i[0]
                application_id = i[1]
                language_list = translation.db_get_translation_cha_id_app_id(character_id,application_id)
                character_msg = character.db_get_character_id(character_id)
                application_msg = application.db_get_application_id(application_id)
                json_transform = tool.newGet(character_msg,application_msg)
                respon_json.append(json_transform)
            data_count = count
            current_number = page
            page_count = math.ceil(count/int(page_size))
            respon_json = tool.pageResponse(data_count,int(current_number),page_count,int(page_size),respon_json)
            respon_json = json.dumps(respon_json)
        else:
            app_id = application.db_get_id_application(app)['id']
            query,count = translation.db_get_translation_group(page_size,page,app_id)
            for i in query:
                character_id = i[0]
                application_id = i[1]
                language_list = translation.db_get_translation_cha_id_app_id(character_id,application_id)
                character_msg = character.db_get_character_id(character_id)
                application_msg = application.db_get_application_id(application_id)
                json_transform = tool.newGet(character_msg,application_msg)
                respon_json.append(json_transform)
            data_count = count
            current_number = page
            page_count = math.ceil(count/int(page_size))
            respon_json = tool.pageResponse(data_count,int(current_number),page_count,int(page_size),respon_json)
        self.write(respon_json)

    #根据app_id,lan_id,cha_id进行更新
    def post(self,translation_id = None): #
        if translation_id is None:
            raise HTTPError(405)
        request_body = self.request.body.decode('utf-8')
        request_body = json.loads(request_body)
        key_list = []
        for key, value in request_body.items():
            key_list.append(key)
        key_list.sort()
        if key_list != ['app_id', 'cha', 'desc', 'language']:
            raise HTTPError(400, reason="KeyError", log_message="key not exist")
        cha = request_body['cha']
        language = request_body['language']
        desc = request_body['desc']
        app_id = request_body['app_id']
        for key,value in language.items():
            if languages.db_get_language_id(key) == {}:
                raise HTTPError(400, reason="LanguageError", log_message="language not exist")
        if application.db_get_application_id(app_id) == {}:
            raise HTTPError(400, reason="AppError", log_message="app not exist")

        post_flag = character.db_get_id_character(cha)
        if post_flag:
            raise HTTPError(400, reason="InsertDataError", log_message="data exist")

        cha_data = [{"name":cha,"description":desc}]
        cha_response = character.db_insert_character(cha_data)

        respon_json = []
        for i in cha_response:
            response = tool.language2dict(i)
            respon_json.append(response)
        cha_id = respon_json[0]['id']


        translation_list = []
        for key,value in language.items():
            data = {
                "language_id": int(key),
                "application_id": app_id,
                "character_id": cha_id,
                "cha_translation": value
            }
            translation_list.append(data)

        for param in translation_list:
            language_id = param['language_id']
            application_id = param['application_id']
            character_id = param['character_id']
            cha_translation = param['cha_translation']
            if application_id == 0:
                application_id = None
            post_flag = translation.db_get_id_translation(language_id,application_id, character_id)
            if post_flag:
                raise HTTPError(400, reason="InsertDataError", log_message="data exist")

        tran_response = translation.db_insert_translation(translation_list)
        respon_json_a = []
        for i in tran_response:
            response = tool.translation2dict(i)
            respon_json_a.append(response)
        respon_json_a = respon_json + respon_json_a
        respon_json_a = json.dumps(respon_json_a)
        print(respon_json_a)
        self.write(respon_json_a)


    def put(self,translation_id = None): #
        if translation_id is None:
            raise HTTPError(405)
        param = self.request.body.decode('utf-8')
        prarm = json.loads(param)
        character_data = prarm['character']
        application_id = prarm['application']
        language_data = prarm['language']
        respon_json = []

        character_id = character_data['id']
        cha_flag = character.db_get_character_id(character_id)
        if cha_flag:
            name = character_data['name']
            description = character_data['description']
            response = character.db_update_character(character_id, name, description)
            response = tool.language2dict(response)
            respon_json.append(response)
        else:
            raise HTTPError(400, reason="FoundDataError", log_message="character not found data")
        print(respon_json)

        put_data = application.db_get_application_id(application_id)
        if not put_data:
            raise HTTPError(400, reason="FoundDataError", log_message="application not found data")
        print(put_data)

        response_dict = []
        for i in language_data:
            language_id = i['id']
            cha_translation = i['cha_translation']
            if application_id == 0:
                application_id = None
            put_data = translation.db_get_id_translation(language_id, application_id, character_id)
            if put_data:
                response = translation.db_update_translation(language_id, application_id, character_id, cha_translation)
                response = tool.translation2dict(response)
                response_dict.append(response)
            else:
                raise HTTPError(400, reason="FoundDataError", log_message="translation not found data")
        respon_json.append(response_dict)
        respon_json = json.dumps(respon_json)
        self.write(respon_json)

    def delete(self, character_id = None):#删除
        if character_id is None:
            raise HTTPError(405)
        delete_flag = translation.db_get_translation_character_id(character_id)
        if delete_flag:
            delete_data = translation.db_delete_translation_character_id(character_id)
            #respon_json = json.dumps(delete_flag)
            print(delete_flag)
            #self.write(respon_json)
        else:
            raise HTTPError(400, reason="FoundDataError", log_message="not found data translation")

        delete_flag_a = character.db_get_character_id(character_id)
        if delete_flag_a:
            delete_data = character.db_delete_character(character_id)
            delete_flag.append(delete_flag_a)
            respon_json = json.dumps(delete_flag)
            self.write(respon_json)
        else:
            raise HTTPError(400, reason="FoundDataError", log_message="not found data character")


    def write_error(self, status_code, **kwargs):
        exc_info = kwargs.get("exc_info", None)
        exc = exc_info[1]
        if isinstance(exc, HTTPError):
            rsp = {
                "RequestId": 'a',
                "Error": {
                    "Code": exc.reason,
                    "Message": exc.log_message,
                    "Type": "Response"
                }
            }
            self.write(rsp)
            self.finish()




class NewEditTransHandler(BaseHandler):

    def get(self, *args, **kwargs):
        respon_json = []
        page_size = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        app = self.get_argument('app', 'all')
        if app == 'all':
            app_id = 0
            query,count = translation.db_get_translation_group(page_size,page,app_id)
            for i in query:
                character_id = i[0]
                application_id = i[1]
                language_list = translation.db_get_translation_cha_id_app_id(character_id,application_id)
                character_msg = character.db_get_character_id(character_id)
                application_msg = application.db_get_application_id(application_id)
                json_transform = tool.newPutGet(language_list,character_msg,application_msg)

                respon_json.append(json_transform)
            data_count = count
            current_number = page
            page_count = math.ceil(count/int(page_size))
            respon_json = tool.pageResponse(data_count,int(current_number),page_count,int(page_size),respon_json)
            respon_json = json.dumps(respon_json)
        elif app == 'public':
            app_id = None
            query,count = translation.db_get_translation_group(page_size,page,app_id)
            for i in query:
                character_id = i[0]
                application_id = i[1]
                language_list = translation.db_get_translation_cha_id_app_id(character_id,application_id)
                character_msg = character.db_get_character_id(character_id)
                application_msg = application.db_get_application_id(application_id)
                json_transform = tool.newPutGet(language_list,character_msg,application_msg)
                respon_json.append(json_transform)
            data_count = count
            current_number = page
            page_count = math.ceil(count/int(page_size))
            respon_json = tool.pageResponse(data_count,int(current_number),page_count,int(page_size),respon_json)
            respon_json = json.dumps(respon_json)
        else:
            app_id = application.db_get_id_application(app)['id']
            query,count = translation.db_get_translation_group(page_size,page,app_id)
            for i in query:
                character_id = i[0]
                application_id = i[1]
                language_list = translation.db_get_translation_cha_id_app_id(character_id,application_id)
                character_msg = character.db_get_character_id(character_id)
                application_msg = application.db_get_application_id(application_id)
                json_transform = tool.newPutGet(language_list,character_msg,application_msg)
                respon_json.append(json_transform)
            data_count = count
            current_number = page
            page_count = math.ceil(count/int(page_size))
            respon_json = tool.pageResponse(data_count,int(current_number),page_count,int(page_size),respon_json)
        self.write(respon_json)
