# -*- encoding: utf-8 -*-
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from unittest.mock import patch
from app.dal import translation
from app.view.translation import TranslationPageHandler
from app.view.translation import TranslationHandler
from app.view.translation import MultiHandler
from app.view.translation import PublicHandler
import json


class TestTranslationHandler(AsyncHTTPTestCase):

    def get_app(self):
        return Application([(r'/translation/(\d*)', TranslationHandler)])

    @patch('app.dal.translation.db_get_translation_list')
    def test_get_list(self, mock_get_translation_list):
        value = [
            {
                'id': 1,
                'name': 'en'
            },
            {
                'id': 2,
                'name': 'ch_zn'
            }
        ]
        mock_get_translation_list.return_value = value
        response = self.fetch("/translation/")
        self.assertEqual(response.code, 200)
        expected_result = json.dumps([{"id": 1, "name": "en"}, {"id": 2, "name": "ch_zn"}]).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.dal.translation.db_get_translation_id')
    def test_get(self, tool_get_translation_id):
        value = {
                'id': 1,
                'name': 'en'
            }
        tool_get_translation_id.return_value = value
        response = self.fetch("/translation/1")
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.translation2dict')
    @patch('app.dal.translation.db_get_id_translation')
    @patch('app.dal.translation.db_insert_translation')
    def test_post(self, mock_db_insert_translation, mock_db_get_id_translation, mock_translation2dict):
        mock_db_get_id_translation.return_value = {}
        mock_db_insert_translation.return_value = {}
        mock_translation2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/translation/", method='POST', body=json.dumps({"language_id" : 2,"application_id" : 0,"character_id" : 1,"cha_translation" : "zaoshuizaoqsi"}).encode())
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.translation2dict')
    @patch('app.dal.translation.db_get_id_translation')
    @patch('app.dal.translation.db_insert_translation')
    def test_post_error_InsertDataError(self, mock_db_insert_translation, mock_db_get_id_translation, mock_translation2dict):
        mock_db_get_id_translation.return_value = {"id": 1, "name": "en"}
        mock_db_insert_translation.return_value = {}
        mock_translation2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/translation/", method='POST', body=json.dumps({"language_id" : 2,"application_id" : 0,"character_id" : 1,"cha_translation" : "zaoshuizaoqsi"}).encode())
        self.assertEqual(response.code, 400)
        error_msg = {
                "RequestId": "a",
                "Error": {
                            "Code": "InsertDataError",
                            "Message": "data exist",
                            "Type": "Response"
                         }
               }
        expected_result = json.dumps(error_msg).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.translation2dict')
    @patch('app.dal.translation.db_get_id_translation')
    @patch('app.dal.translation.db_insert_translation')
    def test_post_error_KeyError(self, mock_db_insert_translation, mock_db_get_id_translation, mock_translation2dict):
        mock_db_get_id_translation.return_value = {"id": 1, "name": "en"}
        mock_db_insert_translation.return_value = {}
        mock_translation2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/translation/", method='POST', body=json.dumps({"language_id0" : 2,"application_id" : 0,"character_id" : 1,"cha_translation" : "zaoshuizaoqsi"}).encode())
        self.assertEqual(response.code, 400)
        error_msg = {
                    "RequestId": "a",
                    "Error":{
                                "Code": "KeyError",
                                "Message": "key not exist",
                                "Type": "Response"
                            }
                    }
        expected_result = json.dumps(error_msg).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.translation2dict')
    @patch('app.dal.translation.db_get_id_translation')
    @patch('app.dal.translation.db_update_translation')
    def test_put(self, mock_db_update_translation, mock_db_get_id_translation, mock_translation2dict):
        mock_db_get_id_translation.return_value = {"id": 1, "name": "en"}
        mock_db_update_translation.return_value = {}
        mock_translation2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/translation/1", method='PUT', body=json.dumps({"language_id" : 2,"application_id" : 0,"character_id" : 1,"cha_translation" : "zaoshuizaoqsi"}).encode())
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.translation2dict')
    @patch('app.dal.translation.db_get_translation_id')
    @patch('app.dal.translation.db_update_translation')
    def test_put_KeyError(self, mock_db_update_translation, mock_db_get_translation_id, mock_translation2dict):
        mock_db_get_translation_id.return_value = {}
        mock_db_update_translation.return_value = {}
        mock_translation2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/translation/1", method='PUT', body=json.dumps({'name0': 'en'}).encode())
        self.assertEqual(response.code, 400)
        error_msg = {
                    "RequestId": "a",
                    "Error":{
                                "Code": "KeyError",
                                "Message": "key not exist",
                                "Type": "Response"
                            }
                    }
        expected_result = json.dumps(error_msg).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.dal.translation.db_get_id_translation')
    @patch('app.dal.translation.db_delete_translation')
    def test_delete(self, mock_db_delete_translation, mock_db_get_id_translation):
        mock_db_get_id_translation.return_value = {"id": 1, "name": "en"}
        mock_db_delete_translation.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/translation/", method='DELETE', \
                              body=json.dumps({"language_id" : 1,\
                                               "application_id" : 0,"character_id" : 1}).encode(),
                              allow_nonstandard_methods=True)
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.dal.translation.db_get_id_translation')
    @patch('app.dal.translation.db_delete_translation')
    def test_delete_FoundDataError(self, mock_db_delete_translation, mock_db_get_id_translation):
        mock_db_get_id_translation.return_value = {}
        mock_db_delete_translation.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/translation/", method='DELETE',
                              body=json.dumps({"language_id" : 1,"application_id" : 0,"character_id" : 1}).encode(),
                              allow_nonstandard_methods=True)
        self.assertEqual(response.code, 400)
        error_msg = {
                    "RequestId": "a",
                    "Error":{
                                "Code": "FoundDataError",
                                "Message": "not found data",
                                "Type": "Response"
                            }
                    }
        expected_result = json.dumps(error_msg).encode()
        self.assertEqual(response.body, expected_result)




class TestTranslationPageHandler(AsyncHTTPTestCase):

    def get_app(self):
        return Application([(r'/translationPage/', TranslationPageHandler)])

    @patch('app.tools.tool.pageResponse')
    @patch('app.tools.tool.translation2dict')
    @patch('app.dal.translation.db_get_translation_page')
    def test_get_list(self, mock_db_get_translation_page, mock_translation2dict, mock_pageResponse):
        value = [
            {
                'id': 1,
                'name': 'en'
            },
            {
                'id': 2,
                'name': 'ch_zn'
            }
        ]
        mock_db_get_translation_page.return_value = value, 10
        mock_translation2dict.return_value = {"id": 1, "name": "en"}
        page_msg = {
            "total": 16,
            "current_number": 1,
            "page_count": 6,
            "page_size": 3,
            "data": [
                {
                    "id": 2,
                    "translation_id": 1,
                    "application_id": None,
                    "character_id": 2,
                    "cha_translation": "tian",
                    "character": "k_2"
                },
                {
                    "id": 4,
                    "translation_id": 1,
                    "application_id": None,
                    "character_id": 4,
                    "cha_translation": "tian",
                    "character": "k_4"
                },
                {
                    "id": 5,
                    "translation_id": 1,
                    "application_id": None,
                    "character_id": 5,
                    "cha_translation": "tian",
                    "character": "k_5"
                }
            ]
        }
        mock_pageResponse.return_value = page_msg
        response = self.fetch("/translationPage/?page=0&page_size=2")
        self.assertEqual(response.code, 200)
        expected_result = json.dumps(page_msg).encode()
        self.assertEqual(response.body, expected_result)


class TestMultiHandler(AsyncHTTPTestCase):

    def get_app(self):
        return Application([(r"/(p)/([a-zA-Z\_]*)", MultiHandler)])

    @patch('app.dal.languages.db_get_id_language')
    @patch('app.dal.application.db_get_id_application')
    @patch('app.dal.translation.db_get_language_translation')
    def test_get_list(self, mock_db_get_language_translation, mock_db_get_id_application,
                      mock_db_get_id_language):
        value = {
                      "k_web0": "zaoshuizaoqsi",
                      "k_2": "tian",
                }
        mock_db_get_language_translation.return_value = value
        mock_db_get_id_application.return_value = {"id": 1, "name": "web"}
        mock_db_get_id_language.return_value = {"id": 1, "name": "en"}
        response = self.fetch('/p/console', headers = {'Accept-Language':'en'})
        self.assertEqual(response.code, 200)
        expected_result = json.dumps(value).encode()
        self.assertEqual(response.body, expected_result)


class TestPublicHandler(AsyncHTTPTestCase):

    def get_app(self):
        return Application([(r"/", PublicHandler)])

    @patch('app.dal.languages.db_get_id_language')
    @patch('app.dal.translation.db_get_language_translation')
    def test_get_list(self, mock_db_get_language_translation, mock_db_get_id_language):
        value = {
                      "k_web0": "zaoshuizaoqsi",
                      "k_2": "tian",
                }
        mock_db_get_language_translation.return_value = value
        mock_db_get_id_language.return_value = {"id": 1, "name": "en"}
        response = self.fetch('/', headers = {'Accept-Language':'en'})
        self.assertEqual(response.code, 200)
        expected_result = json.dumps(value).encode()
        self.assertEqual(response.body, expected_result)