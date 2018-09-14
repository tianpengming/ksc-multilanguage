from app.tools import tool
from sqlClass import Character
from app.dal.base import DBSession




def db_get_character_list():
    session = DBSession()
    character_list = session.query(Character).all()
    respon_dict = []
    if character_list:
        for i in character_list:
            json_transform = tool.language2dict(i)
            respon_dict.append(json_transform)
    else:
        respon_dict = []
    session.commit()
    session.close()
    return respon_dict


def db_get_character_id(character_id):
    session = DBSession()
    character_list = session.query(Character).filter(Character.id == character_id).first()
    if character_list:
        respon_dict = tool.language2dict(character_list)
    else:
        respon_dict = {}
    session.commit()
    session.close()
    return respon_dict


def db_get_character_page(page_size,page):
    session = DBSession()
    count = session.query(Character).count()
    query = session.query(Character).limit(page_size).offset((int(page)-1) * int(page_size))
    session.commit()
    session.close()
    return query,count


#通过name查询
def db_get_id_character(name):
    session = DBSession()
    post_flag = session.query(Character).filter(Character.name == name).first()
    if post_flag:
        respon_dict = tool.language2dict(post_flag)
    else:
        respon_dict = 0
    session.commit()
    session.close()
    return respon_dict


def db_insert_character(character_list):
    session = DBSession()
    response = []
    for i in character_list:
        character = Character(name = i['name'], description = i['description'])
        session.add(character)
        response.append(character)
        session.commit()

    return response

def db_delete_character(character_id):
    session = DBSession()
    delete_data = session.query(Character).filter(Character.id == character_id). \
        delete(synchronize_session=False)
    session.commit()
    session.close()
    return 1


def db_update_character(character_id,name,description):
    session = DBSession()
    query = session.query(Character).filter(Character.id == character_id)
    query.update({Character.name: name,Character.description:description}, synchronize_session=False) #找到id更新
    response = query.first()
    session.commit()
    return response
