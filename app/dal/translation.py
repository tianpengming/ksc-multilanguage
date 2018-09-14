from app.tools import tool
from sqlClass import Translation
from app.dal.base import DBSession



#获取translation表list
def db_get_translation_list():
    session = DBSession()
    translation_list = session.query(Translation).all()
    respon_dict = []
    if translation_list:
        for i in translation_list:
            json_transform = tool.translation2dict(i)
            respon_dict.append(json_transform)
    else:
        respon_dict = []
    session.commit()
    session.close()
    return respon_dict


#通过id查询translation表
def db_get_translation_id(translation_id):
    session = DBSession()
    translation_list = session.query(Translation).filter(Translation.id == translation_id).first()
    if translation_list:
        respon_dict = tool.translation2dict(translation_list)
    else:
        respon_dict = []
    session.commit()
    session.close()
    return respon_dict


#分页查询translation表
def db_get_translation_page(page_size,page):
    session = DBSession()
    count = session.query(Translation).count()
    query = session.query(Translation).order_by(Translation.application_id).limit(page_size).offset((int(page)-1) * int(page_size))
    session.commit()
    session.close()
    return query,count


def db_get_translation_group(page_size,page,app_id):
    session = DBSession()
    if app_id == 0:
        count = session.query(Translation.character_id,Translation.application_id).\
            order_by(Translation.character_id,Translation.application_id).\
            group_by(Translation.character_id,Translation.application_id).count()
        #query = session.query(Translation).order_by(Translation.application_id).limit(page_size).offset((int(page)-1) * int(page_size))
        query = session.query(Translation.character_id,Translation.application_id).\
            order_by(Translation.character_id,Translation.application_id).\
            group_by(Translation.character_id,Translation.application_id).limit(page_size).offset((int(page)-1) * int(page_size)).all()
    else:
        count = session.query(Translation.character_id, Translation.application_id).filter(Translation.application_id == app_id).\
            order_by(Translation.character_id, Translation.application_id). \
            group_by(Translation.character_id, Translation.application_id).count()
        # query = session.query(Translation).order_by(Translation.application_id).limit(page_size).offset((int(page)-1) * int(page_size))
        query = session.query(Translation.character_id, Translation.application_id). filter(Translation.application_id == app_id).\
            order_by(Translation.character_id, Translation.application_id). \
            group_by(Translation.character_id, Translation.application_id).limit(page_size).offset(
            (int(page) - 1) * int(page_size)).all()
    session.commit()
    session.close()
    return query,count


#通过language_id,application_id,character_id查询表
def db_get_id_translation(language_id, application_id , character_id):
    session = DBSession()
    post_flag = session.query(Translation).filter(Translation.language_id == language_id, \
                                                  Translation.application_id == application_id ,\
                                                    Translation.character_id == character_id).first()
    if post_flag:
        respon_dict = tool.translation2dict(post_flag)
    else:
        respon_dict = 0
    session.commit()
    session.close()
    return respon_dict


#通过character_id查询表
def db_get_translation_character_id(character_id):
    session = DBSession()
    translation_list = session.query(Translation).filter(Translation.character_id == character_id).all()
    respon_dict = []
    if translation_list:
        for i in translation_list:
            json_transform = tool.translation2dict(i)
            respon_dict.append(json_transform)
    else:
        respon_dict = []
    session.commit()
    session.close()
    return respon_dict


#插入
def db_insert_translation(translation_list):
    session = DBSession()
    response = []
    for param in translation_list:
        language_id = param['language_id']
        application_id = param['application_id']
        character_id = param['character_id']
        cha_translation = param['cha_translation']
        translation = Translation(language_id=language_id, application_id=application_id, \
                                  character_id=character_id, cha_translation=cha_translation)
        session.add(translation)
        response.append(translation)
    session.commit()
    return response


#删除
def db_delete_translation(language_id, application_id, character_id):
    session = DBSession()
    delete_data = session.query(Translation).filter(Translation.language_id == language_id, \
                                                  Translation.application_id == application_id ,\
                                                    Translation.character_id == character_id). \
        delete(synchronize_session=False)
    session.commit()
    session.close()
    return 1

#通过character_id删除所有
def db_delete_translation_character_id(character_id):
    session = DBSession()
    delete_data = session.query(Translation).filter(Translation.character_id == character_id). \
        delete(synchronize_session=False)
    session.commit()
    session.close()
    return 1



#更新
def db_update_translation(language_id, application_id, character_id,cha_translation):
    session = DBSession()
    query = session.query(Translation).filter(Translation.language_id == language_id, \
                                                  Translation.application_id == application_id ,\
                                                    Translation.character_id == character_id)
    query.update({Translation.cha_translation: cha_translation}, synchronize_session=False) #找到id更新
    response = query.first()
    session.commit()
    return response


#查找某语言某应用的所有站位符对应的翻译
def db_get_language_translation(language_id,application_id):
    session = DBSession()
    translation_list = session.query(Translation).filter(\
        Translation.language_id == language_id,Translation.application_id == application_id).all()
    respon_dict = {}
    if translation_list:
        for i in translation_list:
            respon_dict[i.character.name] = i.cha_translation
    else:
        respon_dict = {}
    session.commit()
    session.close()
    return respon_dict


#查找某语言某应用的所有站位符对应的翻译
def db_get_translation_cha_id_app_id(character_id,application_id):
    session = DBSession()
    translation_list = session.query(Translation).filter(\
        Translation.character_id == character_id,Translation.application_id == application_id).order_by(Translation.language_id).all()
    respon_dict = []
    if translation_list:
        for i in translation_list:
            json_transform = tool.lan(i)
            respon_dict.append(json_transform)
    else:
        respon_dict = []
    session.commit()
    session.close()
    return respon_dict

