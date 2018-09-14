# -*- encoding: utf-8 -*-
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from unittest.mock import patch
from app.dal import application
from app.view.application import ApplicationPageHandler
from app.view.application import ApplicationHandler
import json


class TestApplicationHandler(AsyncHTTPTestCase):

    def get_app(self):
        return Application([(r'/application/(\d*)', ApplicationHandler)])

    @patch('app.dal.application.db_get_application_list')
    def test_get_list(self, mock_get_application_list):
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
        mock_get_application_list.return_value = value
        response = self.fetch("/application/")
        self.assertEqual(response.code, 200)
        expected_result = json.dumps([{"id": 1, "name": "en"}, {"id": 2, "name": "ch_zn"}]).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.dal.application.db_get_application_id')
    def test_get(self, tool_get_application_id):
        value = {
                'id': 1,
                'name': 'en'
            }
        tool_get_application_id.return_value = value
        response = self.fetch("/application/1")
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.language2dict')
    @patch('app.dal.application.db_get_id_application')
    @patch('app.dal.application.db_insert_application')
    def test_post(self, mock_db_insert_application, mock_db_get_id_application, mock_language2dict):
        mock_db_get_id_application.return_value = {}
        mock_db_insert_application.return_value = {}
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/application/", method='POST', body=json.dumps({'name': 'en'}).encode())
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.language2dict')
    @patch('app.dal.application.db_get_id_application')
    @patch('app.dal.application.db_insert_application')
    def test_post_error_InsertDataError(self, mock_db_insert_application, mock_db_get_id_application, mock_language2dict):
        mock_db_get_id_application.return_value = {"id": 1, "name": "en"}
        mock_db_insert_application.return_value = {}
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/application/", method='POST', body=json.dumps({'name': 'en'}).encode())
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
    @patch('app.dal.application.db_get_id_application')
    @patch('app.dal.application.db_insert_application')
    def test_post_error_KeyError(self, mock_db_insert_application, mock_db_get_id_application, mock_language2dict):
        mock_db_get_id_application.return_value = {"id": 1, "name": "en"}
        mock_db_insert_application.return_value = {}
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/application/", method='POST', body=json.dumps({'name0': 'en'}).encode())
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
    @patch('app.dal.application.db_get_id_application')
    @patch('app.dal.application.db_update_application')
    def test_put(self, mock_db_update_application, mock_db_get_id_application, mock_language2dict):
        mock_db_get_id_application.return_value = {"id": 1, "name": "en"}
        mock_db_update_application.return_value = {}
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/application/1", method='PUT', body=json.dumps({'name': 'en'}).encode())
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.tools.tool.language2dict')
    @patch('app.dal.application.db_get_application_id')
    @patch('app.dal.application.db_update_application')
    def test_put_KeyError(self, mock_db_update_application, mock_db_get_application_id, mock_language2dict):
        mock_db_get_application_id.return_value = {}
        mock_db_update_application.return_value = {}
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/application/1", method='PUT', body=json.dumps({'name0': 'en'}).encode())
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

    @patch('app.dal.application.db_get_application_id')
    @patch('app.dal.application.db_delete_application')
    def test_delete(self, mock_db_delete_application, mock_db_get_application_id):
        mock_db_get_application_id.return_value = {"id": 1, "name": "en"}
        mock_db_delete_application.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/application/1", method='DELETE')
        self.assertEqual(response.code, 200)
        expected_result = json.dumps({"id": 1, "name": "en"}).encode()
        self.assertEqual(response.body, expected_result)

    @patch('app.dal.application.db_get_application_id')
    @patch('app.dal.application.db_delete_application')
    def test_delete_FoundDataError(self, mock_db_delete_application, mock_db_get_application_id):
        mock_db_get_application_id.return_value = {}
        mock_db_delete_application.return_value = {"id": 1, "name": "en"}
        response = self.fetch("/application/1", method='DELETE')
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




class TestApplicationPageHandler(AsyncHTTPTestCase):

    def get_app(self):
        return Application([(r'/applicationPage/', ApplicationPageHandler)])

    @patch('app.tools.tool.pageResponse')
    @patch('app.tools.tool.language2dict')
    @patch('app.dal.application.db_get_application_page')
    def test_get_list(self, mock_db_get_application_page, mock_language2dict, mock_pageResponse):
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
        mock_db_get_application_page.return_value = value, 10
        mock_language2dict.return_value = {"id": 1, "name": "en"}
        page_msg = {
            "total": 16,
            "current_number": 1,
            "page_count": 6,
            "page_size": 3,
            "data": [
                {
                    "id": 2,
                    "application_id": 1,
                    "application_id": None,
                    "character_id": 2,
                    "cha_translation": "tian",
                    "character": "k_2"
                },
                {
                    "id": 4,
                    "application_id": 1,
                    "application_id": None,
                    "character_id": 4,
                    "cha_translation": "tian",
                    "character": "k_4"
                },
                {
                    "id": 5,
                    "application_id": 1,
                    "application_id": None,
                    "character_id": 5,
                    "cha_translation": "tian",
                    "character": "k_5"
                }
            ]
        }
        mock_pageResponse.return_value = page_msg
        response = self.fetch("/applicationPage/?page=0&page_size=2")
        self.assertEqual(response.code, 200)
        expected_result = json.dumps(page_msg).encode()
        self.assertEqual(response.body, expected_result)
