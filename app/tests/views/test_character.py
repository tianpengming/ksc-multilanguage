# -*- encoding: utf-8 -*-
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from unittest.mock import patch
from app.dal import character
from app.view.character import CharacterPageHandler
from app.view.character import CharacterHandler
import json


class TestCharacterHandler(AsyncHTTPTestCase):

    def get_app(self):
        return Application([(r'/character/(\d*)', CharacterHandler)])

    @patch('app.dal.character.db_get_character_list')
    def test_get_list(self, mock_get_character_list):
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
        mock_get_character_list.return_value = value
        response = self.fetch("/character/")
        self.assertEqual(response.code, 200)
        expected_result = json.dumps([{"id": 1, "name": "en"}, {"id": 2, "name": "ch_zn"}]).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.dal.character.db_get_character_id')
    def test_get(self, tool_get_character_id):
        value = {
                'id': 1,
                'name': 'en'
            }
        tool_get_character_id.return_value = value
        response = self.fetch("/character/1")
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.language2dict')
    @patch('app.dal.character.db_get_id_character')
    @patch('app.dal.character.db_insert_character')
    def test_post(self, mock_db_insert_character, mock_db_get_id_character, mock_language2dict):
        mock_db_get_id_character.return_value = {}
        mock_db_insert_character.return_value = {}
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/character/", method='POST', body=json.dumps({'name': 'en'}).encode())
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.language2dict')
    @patch('app.dal.character.db_get_id_character')
    @patch('app.dal.character.db_insert_character')
    def test_post_error_InsertDataError(self, mock_db_insert_character, mock_db_get_id_character, mock_language2dict):
        mock_db_get_id_character.return_value = {"id": 1, "name": "en"}
        mock_db_insert_character.return_value = {}
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/character/", method='POST', body=json.dumps({'name': 'en'}).encode())
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

    @patch('app.tools.tool.language2dict')
    @patch('app.dal.character.db_get_id_character')
    @patch('app.dal.character.db_insert_character')
    def test_post_error_KeyError(self, mock_db_insert_character, mock_db_get_id_character, mock_language2dict):
        mock_db_get_id_character.return_value = {"id": 1, "name": "en"}
        mock_db_insert_character.return_value = {}
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/character/", method='POST', body=json.dumps({'name0': 'en'}).encode())
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

    @patch('app.tools.tool.language2dict')
    @patch('app.dal.character.db_get_id_character')
    @patch('app.dal.character.db_update_character')
    def test_put(self, mock_db_update_character, mock_db_get_id_character, mock_language2dict):
        mock_db_get_id_character.return_value = {"id": 1, "name": "en"}
        mock_db_update_character.return_value = {}
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/character/1", method='PUT', body=json.dumps({'name': 'en'}).encode())
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.language2dict')
    @patch('app.dal.character.db_get_character_id')
    @patch('app.dal.character.db_update_character')
    def test_put_KeyError(self, mock_db_update_character, mock_db_get_character_id, mock_language2dict):
        mock_db_get_character_id.return_value = {}
        mock_db_update_character.return_value = {}
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/character/1", method='PUT', body=json.dumps({'name0': 'en'}).encode())
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

    @patch('app.dal.character.db_get_character_id')
    @patch('app.dal.character.db_delete_character')
    def test_delete(self, mock_db_delete_character, mock_db_get_character_id):
        mock_db_get_character_id.return_value = {"id": 1, "name": "en"}
        mock_db_delete_character.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/character/1", method='DELETE')
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.dal.character.db_get_character_id')
    @patch('app.dal.character.db_delete_character')
    def test_delete_FoundDataError(self, mock_db_delete_character, mock_db_get_character_id):
        mock_db_get_character_id.return_value = {}
        mock_db_delete_character.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/character/1", method='DELETE')
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




class TestCharacterPageHandler(AsyncHTTPTestCase):

    def get_app(self):
        return Application([(r'/characterPage/', CharacterPageHandler)])

    @patch('app.tools.tool.pageResponse')
    @patch('app.tools.tool.language2dict')
    @patch('app.dal.character.db_get_character_page')
    def test_get_list(self, mock_db_get_character_page, mock_language2dict, mock_pageResponse):
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
        mock_db_get_character_page.return_value = value, 10
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        page_msg = {
            "total": 16,
            "current_number": 1,
            "page_count": 6,
            "page_size": 3,
            "data": [
                {
                    "id": 2,
                    "character_id": 1,
                    "application_id": None,
                    "character_id": 2,
                    "cha_translation": "tian",
                    "character": "k_2"
                },
                {
                    "id": 4,
                    "character_id": 1,
                    "application_id": None,
                    "character_id": 4,
                    "cha_translation": "tian",
                    "character": "k_4"
                },
                {
                    "id": 5,
                    "character_id": 1,
                    "application_id": None,
                    "character_id": 5,
                    "cha_translation": "tian",
                    "character": "k_5"
                }
            ]
        }
        mock_pageResponse.return_value = page_msg
        response = self.fetch("/characterPage/?page=0&page_size=2")
        self.assertEqual(response.code, 200)
        expected_result = json.dumps(page_msg).encode()
        self.assertEqual(response.body, expected_result)
