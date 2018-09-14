def language2dict(std):
    """
    语言class转dict
    :param std:
    :return:
    """
    try:
        std.identification
    except AttributeError:
        return {
            'id': std.id,
            'name': std.name,
            'description':std.description,
        }
    else:
        return {
            'id': std.id,
            'name': std.name,
            'description':std.description,
            'identification': std.identification
        }


def translation2dict(std):
    """
    translation表转dict
    :param std:
    """
    return {
        'id': std.id,
        'language_id':std.language_id,
        'application_id':std.application_id,
        'character_id':std.character_id,
        'cha_translation':std.cha_translation,
        'character':std.character.name
    }



def pageResponse(data_count,current_number,page_count,page_size,data):
    return{
        'total':data_count,
        'data':data
    }

def lan(std):
    """
    translation表转dict
    :param std:
    """
    language = {
        'id': std.language_id,
        'name':std.language.name,
        'cha_translation':std.cha_translation
    }
    return language

def newGet(character_msg,application_msg):
    """
    translation表转dict
    :param std:
    """
    return {
        'id': character_msg['id'],
        'name': character_msg['name'],
        'app_id': application_msg['id'],
        'app_name':application_msg['name'],
        'description':character_msg['description']
        }


def newPutGet(translantion_list,character_msg,application_msg):
    """
    translation表转dict
    :param std:
    """
    return {
        'id': character_msg['id'],
        'name': character_msg['name'],
        'app_id': application_msg['id'],
        'app_name': application_msg['name'],
        'language':translantion_list
    }
'''
class DatabaseException(Exception):
    def __init__(self,err='数据库错误'):
        Exception.__init__(self,err)
'''


'''
def multitrans2dict(std):
    """
    多国语言翻译查询结果转dict
    :param std:
    :return:
    """
    if std.application == None:
        return {
            std.character.name :std.cha_translation,
            "language":std.language.name,
            "application":"public"
        }
    return {
        std.character.name :std.cha_translation,
        "language":std.language.name,
        "application":std.application.name
    }
'''