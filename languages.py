import textwrap
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import HTTPError
from tornado.options import define, options
import tornado

from sqlalchemy import Column, String,Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.query import orm_exc
import json
import tornado.autoreload
define("port", default=8000, help="run on the given port", type=int)
settings = {'debug' : True}
#---------------------------------------------------------------------------------------------


def language2dict(std):
    return {
        'id': std.id,
        'name': std.name,
    }


def httpErrorResponse(std):
    return {
            "RequestId":'a',
            "Error":{
                "Type":'Response',
                "Code":"MissingParameter",
                'Message':'缺少必要信息'
            }
        }


def httpInsertResponse(std):
    return{
        'message':'插入成功',
        'data':std
    }


def httpDeleteResponse(std):
    return{
        'message':'删除成功',
        'data':std
    }

def httpPutResponse(language_id,std,std1):
    return{
        'message':'更新成功',
        'origin_data':{
            'id':language_id,
            'name':std
        },
        'current_data':std1
    }


class DatabaseException(Exception):
    def __init__(self,err='数据库错误'):
        Exception.__init__(self,err)


#---------------------------------------------------------------------------------------------
#错误状态码
# 没找到数据 status_code = 0,
# 插入数据已经存在 status_code = 1
# 键错误 status_code = 2


# 创建对象的基类:
Base = declarative_base()


# 定义Language对象:
class Language(Base):
    # 表的名字:
    __tablename__ = 'language'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    name = Column(String(20))


engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/multiLanguage')
DBSession = sessionmaker(bind=engine)

#---------------------------------------------------------------------------------------------


#language表
class LanguageHandler(tornado.web.RequestHandler):
    def get(self,language_id = ''):   #list和指定id查询
        session = DBSession()
        respon_json = []
        print('-----------------')
        print(type(language_id))
        print(language_id)
        if language_id == '':
            language_list = session.query(Language).all()
            if language_list:
                for i in language_list:
                    json_transform = language2dict(i)
                    respon_json.append(json_transform)
            else:
                respon_json = []
        else:
            language_list = session.query(Language).filter(Language.id == language_id).first()
            if language_list:
                respon_json = language2dict(language_list)
            else:
                respon_json = []
        session.commit()
        session.close()
        respon_json = json.dumps(respon_json)
        self.write(respon_json)

    def post(self, *args, **kwargs):#增加
        session = DBSession()
        param = self.request.body.decode('utf-8')
        prarm = json.loads(param)
        if 'name' in prarm.keys(): #判断键是否正确
            post_flag = session.query(Language).filter(Language.name == prarm['name']).first()
            if post_flag:
                session.commit()
                session.close()
                raise HTTPError(400, reason="InvalidParamsError", log_message="xixihahah")
                # self.write_error(1)

            else:
                language = Language(name=prarm['name'])
                session.add(language)
                response = httpInsertResponse(prarm)     #返回添加成功消息
                session.commit()
                session.close()
                respon_json = json.dumps(response)
                self.write(respon_json)  # 需要修改
        else:
            session.commit()
            session.close()
            self.write_error(2)

    def delete(self, language_id = None):#删除
        if language_id is None:
            raise HTTPError(405)
        session = DBSession()
        delete_flag = session.query(Language).filter(Language.id == language_id).first()
        if delete_flag:
            delete_data = session.query(Language).filter(Language.id == language_id). \
                delete(synchronize_session=False)
            response = httpDeleteResponse(language2dict(delete_flag))
            session.commit()
            session.close()
            respon_json = json.dumps(response)
            self.write(respon_json)  # 需要修改
        else:
            session.commit()
            session.close()
            self.write_error(0)

    def put(self,language_id = None): #更新
        if language_id is None:
            raise HTTPError(405)
        session = DBSession()
        param = self.request.body.decode('utf-8')
        prarm = json.loads(param)
        if 'name' in prarm.keys():  # 判断键是否正确
            put_data = session.query(Language).filter(Language.id == language_id).first()
            if put_data:
                session.query(Language).filter(Language.id == language_id).update({Language.name: prarm['name']}, synchronize_session=False) #找到id更新
                response = httpPutResponse(language_id,prarm,language2dict(put_data))
                session.commit()
                session.close()
                respon_json = json.dumps(response)
                self.write(respon_json)  # 需要修改
            else:
                session.commit()
                session.close()
                self.write_error(0)
        else:
            session.commit()
            session.close()
            raise HTTPError()

    def write_error(self,status_code, **kwargs):

        exc_info = kwargs.get("exc_info", None)
        exc = exc_info[1]

        if isinstance(exc, HTTPError):
            rsp = {
                "Code": exc.reason,
                "Message": exc.log_message
            }
            self.write(rsp)
            self.finish()


        if status_code == 0:
            error_message = {
                'message':'no data'
            }
            error_message = json.dumps(error_message)
            self.write(error_message)
        elif status_code == 1:
            error_message = {
                'message':'data exist no need to insert'
            }
            error_message = json.dumps(error_message)
            self.write(error_message)
        elif status_code == 2:
            error_message = {
                'message':'key error'
            }
            error_message = json.dumps(error_message)
            self.write(error_message)

    def patch(self, *args, **kwargs):
        raise HTTPError(405)


class LanguagePageHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        respon_json = []
        query = session.query(Language)
        page_size = self.get_argument('page_size')
        page = self.get_argument('page')
        if page_size:
            query = query.limit(page_size)
        if page:
            query = query.offset(page * page_size)
        for i in query:
            json_transform = language2dict(i)
            respon_json.append(json_transform)
        respon_json = json.dumps(respon_json)
        self.write(respon_json)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/language/(\w*)", LanguageHandler),
            (r"/languagePage/(\w*)", LanguagePageHandler)
        ],**settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()






