import unittest
from app.tools.tool import language2dict
from app.tools.tool import translation2dict
from app.tools.tool import pageResponse
import sqlClass


class Translation_test():
    pass

class Charater_test():
    pass

class Tools(unittest.TestCase):

    def test_language2dict(self):
        language = sqlClass.Language()
        language.id = 1
        language.name = 'en'
        self.assertEquals(language2dict(language), dict(id = 1, name = 'en'))



    def test_translation2dict(self):
        translation = Translation_test()
        translation.id = 1
        translation.application_id = 1
        translation.language_id = 1
        translation.character_id = 1
        translation.cha_translation = 'web0'
        character = Charater_test()
        character.name = "k_web0"
        translation.character = character
        self.assertEquals(translation2dict(translation),
                          dict(id = 1, application_id = 1, \
                                language_id = 1, character_id = 1, \
                                cha_translation = 'web0', character = 'k_web0'))


    def test_pageResponse(self):
        self.assertEquals(pageResponse(1,1,1,1,'a'),
            {
                'total':1,
                'current_number':1,
                'page_count':1,
                'page_size':1,
                'data':'a'
            }
        )



