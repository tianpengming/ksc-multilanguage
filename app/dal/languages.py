from app.tools import tool
from sqlClass import Language
from app.dal.base import DBSession



#查询language表list
def db_get_language_list():
    session = DBSession()
    language_list = session.query(Language).all()
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


#通过id查询元素
def db_get_language_id(language_id):
    session = DBSession()
    language_list = session.query(Language).filter(Language.id == language_id).first()
    if language_list:
        respon_dict = tool.language2dict(language_list)
    else:
        respon_dict = {}
    session.commit()
    session.close()
    return respon_dict


#分页查询
def db_get_language_page(page_size,page):
    session = DBSession()
    count = session.query(Language).count()
    query = session.query(Language).limit(page_size).offset((int(page)-1) * int(page_size))
    session.commit()
    session.close()
    return query,count

#插入
def db_insert_language(language_list):
    session = DBSession()
    response = []
    for i in language_list:
        language = Language(name = i['name'], description = i['description'], identification = i['identification'])
        session.add(language)
        response.append(language)
        session.commit()
    return response


#删除
def db_delete_language(language_id):
    session = DBSession()
    delete_data = session.query(Language).filter(Language.id == language_id). \
        delete(synchronize_session=False)
    session.commit()
    session.close()
    return 1


#更新
def db_update_language(language_id,name,description):
    session = DBSession()
    query = session.query(Language).filter(Language.id == language_id)
    query.update({Language.name: name,Language.description: description}, synchronize_session=False) #找到id更新
    response = query.first()
    session.commit()
    return response


#通过lang-name获取id
def db_get_id_language(accept_language):
    session = DBSession()
    language_list = session.query(Language).filter(Language.name == accept_language).first()
    if language_list:
        respon_dict = tool.language2dict(language_list)
    else:
        respon_dict = {}
    session.commit()
    session.close()
    return respon_dict
