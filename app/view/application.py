from tornado.web import HTTPError
from app.dal import application
from app.tools import tool
import tornado.web
import json
import math
from app.view.basehandler import BaseHandler


class ApplicationHandler(BaseHandler):
    """
    处理application表的handle
    """
    def get(self,application_id = ''):
        """
        :param application_id: application表的id
        :return: application表查询的所有数据的list或者某id数据
        """
        if application_id == '':
            respon_json = application.db_get_application_list()
        else:
            respon_json = application.db_get_application_id(application_id)
        respon_json = json.dumps(respon_json)
        self.write(respon_json)

    def post(self, *args, **kwargs):
        """
        添加数据,name字段在body中传递,插入到表中
        :return: 插入成功,或者错误消息
        """
        param_list = self.request.body.decode('utf-8')
        param_list = json.loads(param_list)
        for param in param_list:
            if 'name' not in param.keys():
                raise HTTPError(400, reason="KeyError", log_message="key not exist")
        for param in param_list:
            name = param['name']
            post_flag = application.db_get_id_application(name)
            if post_flag:
                raise HTTPError(400, reason="InsertDataError", log_message="data exist")
        response = application.db_insert_application(param_list)
        respon_json = []
        for i in response:
            response = tool.language2dict(i)
            respon_json.append(response)
        respon_json = json.dumps(respon_json)
        self.write(respon_json)


    def delete(self, application_id = None):
        """
        删除数据
        :param application_id:删除表中该id数据
        :return: 删除成功或者错误
        """
        if application_id is None:
            raise HTTPError(405)
        delete_flag = application.db_get_application_id(application_id)
        if delete_flag:
            delete_data = application.db_delete_application(application_id)
            respon_json = json.dumps(delete_flag)
            self.write(respon_json)
        else:
            raise HTTPError(400, reason="FoundDataError", log_message="not found data")

    def put(self,application_id = None):
        """
        更新数据
        :param application_id:
        :return:
        """
        if application_id is None:
            raise HTTPError(405)
        param = self.request.body.decode('utf-8')
        prarm = json.loads(param)
        if 'name' in prarm.keys():  # 判断键是否正确
            put_data = application.db_get_application_id(application_id)
            if put_data:
                name = prarm['name']
                description = prarm['description']
                response = application.db_update_application(application_id,name,description)
                response = tool.language2dict(response)
                respon_json = json.dumps(response)
                self.write(respon_json)  # 需要修改
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


class ApplicationPageHandler(BaseHandler):
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
        query,count = application.db_get_application_page(page_size,page)
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
