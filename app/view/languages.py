from tornado.web import HTTPError
from app.dal import languages
from app.tools import tool
import tornado.web
import json
import math
from app.view.basehandler import BaseHandler


class LanguageHandler(BaseHandler):
    """
    处理language表的handle
    """
    def get(self,language_id = ''):
        """
        查询
        :param language_id:
        :return: id对应的数据或者全部数据
        """
        respon_json = []
        if language_id == '':
            respon_json = languages.db_get_language_list()
        else:
            respon_json = languages.db_get_language_id(language_id)
        respon_json = json.dumps(respon_json)
        self.write(respon_json)

    def post(self, *args, **kwargs):
        """
        增加
        """
        param_list = self.request.body.decode('utf-8')
        param_list = json.loads(param_list)
        for param in param_list:
            if 'name' not in param.keys():
                raise HTTPError(400, reason="KeyError", log_message="key not exist")
        for param in param_list:
            name = param['name']
            post_flag = languages.db_get_id_language(name)
            if post_flag:
                raise HTTPError(400, reason="InsertDataError", log_message="data exist")
        response = languages.db_insert_language(param_list)
        respon_json = []
        for i in response:
            response = tool.language2dict(i)
            respon_json.append(response)
        respon_json = json.dumps(respon_json)
        self.write(respon_json)

    def delete(self, language_id = None):
        """
        删除
        :param language_id:
        :return: 删除成功或者失败
        """
        if language_id is None:
            raise HTTPError(405)
        delete_flag = languages.db_get_language_id(language_id)
        if delete_flag:
            delete_data = languages.db_delete_language(language_id)
            respon_json = json.dumps(delete_data)
            self.write(respon_json)
        else:
            raise HTTPError(400, reason="FoundDataError", log_message="not found data")

    def put(self,language_id = None):
        """
        更新,id对应的数据
        :param language_id:
        :return: 更新成功或者失败
        """
        if language_id is None:
            raise HTTPError(405)
        param = self.request.body.decode('utf-8')
        prarm = json.loads(param)
        if 'name' in prarm.keys():  # 判断键是否正确
            put_data = languages.db_get_language_id(language_id)
            if put_data:
                name = prarm['name']
                description = prarm['description']
                response = languages.db_update_language(language_id,name,description)
                response = tool.language2dict(response)
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


class LanguagePageHandler(BaseHandler):
    """
    处理请求返回分页的url
    """
    def get(self, *args, **kwargs):
        """
        获取分页数据
        :param args:　‘limit’ 每页数目，‘page’ 页数
        :param kwargs:
        :return: 分页数据
        """
        respon_json = []
        page_size = self.get_argument('limit', 10)
        page = self.get_argument('page', 1)
        query, count = languages.db_get_language_page(page_size,page)
        print(type(query))
        for i in query:
            json_transform = tool.language2dict(i)
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
                    "Message": exc.log_message
                }
            }
            self.write(rsp)
            self.finish()
