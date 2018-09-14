from app.tools import tool
from sqlClass import Application


from app.dal.base import DBSession



#application-list
def db_get_application_list():
    session = DBSession()
    language_list = session.query(Application).all()
    respon_dict = []
    if language_list:
        for i in language_list:
            json_transform = tool.language2dict(i)
            respon_dict.append(json_transform)
    else:
        respon_dict = []
    session.commit()
    session.close()
    return respon_dict


#通过id查询
def db_get_application_id(application_id):
    session = DBSession()
    language_list = session.query(Application).filter(Application.id == application_id).first()
    if language_list:
        respon_dict = tool.language2dict(language_list)
    else:
        respon_dict = {}
    session.commit()
    session.close()
    return respon_dict


#分页
def db_get_application_page(page_size,page):
    session = DBSession()
    count = session.query(Application).count()
    query = session.query(Application).limit(page_size).offset((int(page)-1)* int(page_size))
    session.commit()
    session.close()
    return query,count


#插入application
def db_insert_application(application_list):
    session = DBSession()
    response = []
    for i in application_list:
        application = Application(name = i['name'], description = i['description'], identification = i['identification'])
        session.add(application)
        response.append(application)
        session.commit()
    return response


#删除
def db_delete_application(language_id):
    session = DBSession()
    delete_data = session.query(Application).filter(Application.id == language_id). \
        delete(synchronize_session=False)
    session.commit()
    session.close()
    return 1


#更新
def db_update_application(language_id,name,description):
    session = DBSession()
    query = session.query(Application).filter(Application.id == language_id)
    query.update({Application.name: name,Application.description: description}, synchronize_session=False) #找到id更新
    response = query.first()
    session.commit()
    return response


#通过name查询
def db_get_id_application(application_identification):
    session = DBSession()
    language_list = session.query(Application).filter(Application.identification == application_identification).first()
    if language_list:
        respon_dict = tool.language2dict(language_list)
    else:
        respon_dict = {}
    print(respon_dict)
    session.commit()
    session.close()
    return respon_dict