import textwrap
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import tornado

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#---------------------------------------------------------------------------------------------
import json
def application2dict(std):
    return {
        'id': std.id,
        'name': std.name,
    }
#---------------------------------------------------------------------------------------------
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义Language对象:
class Application(Base):
    # 表的名字:
    __tablename__ = 'application'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/multiLanguage')
DBSession = sessionmaker(bind=engine)

#---------------------------------------------------------------------------------------------

define("port", default=8000, help="run on the given port", type=int)
#language表
class LanguageHandler(tornado.web.RequestHandler):
    def get(self,application_id = ''):   #list和指定id查询
        session = DBSession()
        respon_json = []
        if application_id == '':
            language_list = session.query(Application).all()
            print(session.query(Application).all())
            for i in language_list:
                json_transform = language2dict(i)
                respon_json.append(json_transform)
        else:
            language_list = session.query(Application).filter(Application.id == application_id).all()
            for i in language_list:
                json_transform = language2dict(i)
                respon_json.append(json_transform)
        session.commit()
        session.close()
        respon_json = json.dumps(respon_json)
        self.write(respon_json)
    def post(self, *args, **kwargs):#增加
        session = DBSession()
        param = self.request.body.decode('utf-8')
        prarm = json.loads(param)
        Application(name=prarm[name])
        session.add(Application)
        session.commit()
        session.close()
        self.write('200') #需要修改

    def delete(self,application_id = ''):#删除
        session = DBSession()
        sess.query(Application).filter(Application.id == application_id). \
            delete(synchronize_session=False)
        session.commit()
        session.close()
        self.write('200') #需要修改

    def put(self,application_id = ''): #更新
        session = DBSession()
        param = self.request.body.decode('utf-8')
        prarm = json.loads(param)
        sess.query(Application).filter(Application.id == application_id). \
            update({Application.name: prarm[name]}, synchronize_session=False)
        session.commit()
        session.close()
        self.write('200') #需要修改

    def patch(self, *args, **kwargs):
        raise HTTPError(405)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/language/(\w|\s{0})", LanguageHandler),
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()