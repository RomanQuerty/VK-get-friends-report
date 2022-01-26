import unittest
import json
import csv
from random import randint
from shutil import rmtree

from vk_api_handler import VkApiHandler
from saver import Saver, WrongParameterValueError
import config
from report_creator import create_report


# https://api.vk.com/method/friends.get?v=5.131&access_token=92f0f33109fd7904157268512b3d13811321d923c0555ddd534caed5ffa4c8007b8dfb820b2b082179d3a

# https://oauth.vk.com/authorize?client_id=1&display=page&redirect_uri=http://example.com/callback&scope=friends&response_type=token&v=5.131&state=123456

class TestVkApiHandler(unittest.TestCase):

    def setUp(self):
        self.vk_api_handler = VkApiHandler()

    def test_default_configuration(self):
        given_config = self.vk_api_handler.config
        self.assertEqual(given_config['access_token'],
                         config.default_access_token)
        self.assertEqual(given_config['user_id'],
                         config.default_user_id)
        self.assertEqual(given_config['users_in_request'],
                         config.default_users_in_request)

    def test_change_access_token(self):
        new_token_value = randint(1, 999999)
        self.vk_api_handler.change_config_param('access_token',
                                                new_token_value)
        self.assertEqual(self.vk_api_handler.config['access_token'],
                         new_token_value)

    def test_change_user_id(self):
        new_user_id_value = randint(1, 999999)
        self.vk_api_handler.change_config_param('user_id',
                                                new_user_id_value)
        self.assertEqual(self.vk_api_handler.config['user_id'],
                         new_user_id_value)

    def test_change_users_in_request(self):
        new_users_in_req_value = randint(1, 999999)
        self.vk_api_handler.change_config_param('users_in_request',
                                                new_users_in_req_value)
        self.assertEqual(self.vk_api_handler.config['users_in_request'],
                         new_users_in_req_value)

    def test_run_VK_method_1(self):
        """Case with Lindsey Stirling"""
        method_name = 'users.get'
        params = {
            'user_id': 210700286
        }
        response = self.vk_api_handler.run_VK_method(method_name,
                                                     params)
        expected_response_content = {
            "response": [
                {
                    "id": 210700286,
                    "first_name": "Lindsey",
                    "last_name": "Stirling",
                    "can_access_closed": True,
                    "is_closed": False
                }
            ]
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response_content)

    def test_run_VK_method_2(self):
        """Case with Danila Poperechniy"""
        method_name = 'users.get'
        params = {
            'user_id': 10050301
        }
        response = self.vk_api_handler.run_VK_method(method_name,
                                                     params)
        expected_response_content = {
            "response": [
                {
                    "id": 10050301,
                    "first_name": "Данила",
                    "last_name": "Поперечный",
                    "can_access_closed": True,
                    "is_closed": False
                }
            ]
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response_content)

    def test_run_VK_method_3(self):
        """Case with wrong method name"""
        method_name = 'wrong.method.name'
        params = {
            'user_id': 10050301
        }
        with self.assertRaises(Exception):
            response = self.vk_api_handler.run_VK_method(method_name,
                                                         params)

    def test_get_friends_amount_1(self):
        """Case with Pavel Durov"""
        self.vk_api_handler.change_config_param('user_id', 1)  # Durov
        friend_amount = self.vk_api_handler.get_friends_amount()
        expected_friends_amount = 0  # Pavel Durov has 0 friends on VK
        self.assertEqual(friend_amount, expected_friends_amount)

    def test_get_friends_amount_2(self):
        """Case with Lindsey Stirling"""
        self.vk_api_handler.change_config_param('user_id', 210700286)
        friend_amount = self.vk_api_handler.get_friends_amount()
        expected_friends_amount = 1  # Lindsey Stirling has 1 friend
        self.assertEqual(friend_amount, expected_friends_amount)

    def test_get_friends_data_1(self):
        """Case with Pavel Durov"""
        self.vk_api_handler.change_config_param('user_id', 1)
        self.vk_api_handler.change_config_param('users_in_request', 5)
        friends_data = self.vk_api_handler.get_friends_data()
        # We expecting empty result, because Durov has 0 friends in VK
        expected_friends_data = []
        self.assertEqual(friends_data, expected_friends_data)

    def test_get_friends_data_2(self):
        """Case with Lindsey Stirling"""
        self.vk_api_handler.change_config_param('user_id', 210700286)
        self.vk_api_handler.change_config_param('users_in_request', 5)
        friends_data = self.vk_api_handler.get_friends_data()
        friends_data[0].pop('track_code')  # track_code always different
        expected_friends_data = [          # so we delete it from tested
            {                              # data
                "id": 26047,
                "first_name": "Александр",
                "last_name": "Степанов",
                "can_access_closed": False,
                "is_closed": True,
                "sex": 2,
                "city": {
                    "id": 2,
                    "title": "Санкт-Петербург"
                },
                "country": {
                    "title": "Россия",
                    "id": 1
                }
            }
        ]
        self.assertEqual(friends_data, expected_friends_data)


class TestSaver(unittest.TestCase):

    def setUp(self):
        self.saver = Saver()

    def test_default_configuration(self):
        self.assertEqual(self.saver.output_dir,
                         config.default_directory)
        self.assertEqual(self.saver.output_file_name,
                         config.default_output_file_name)
        self.assertEqual(self.saver.output_file_type,
                         config.default_output_file_type)

    def test_change_output_dir(self):
        new_value = randint(1, 999999)
        self.saver.change_param('output_dir', new_value)
        self.assertEqual(self.saver.output_dir, str(new_value))

    def test_change_output_file_name(self):
        new_value = randint(1, 999999)
        self.saver.change_param('output_file_name', new_value)
        self.assertEqual(self.saver.output_file_name, str(new_value))

    def test_change_output_file_type_1(self):
        """Wrong value given"""
        new_value = 'Wrong value'
        with self.assertRaises(WrongParameterValueError):
            self.saver.change_param('output_file_type', new_value)

    def test_change_output_file_type_2(self):
        """json"""
        new_value = 'json'
        self.saver.change_param('output_file_type', new_value)
        self.assertEqual(self.saver.output_file_type, new_value)

    def test_change_output_file_type_3(self):
        """csv"""
        new_value = 'csv'
        self.saver.change_param('output_file_type', new_value)
        self.assertEqual(self.saver.output_file_type, new_value)

    def test_change_output_file_type_4(self):
        """tsv"""
        new_value = 'tsv'
        self.saver.change_param('output_file_type', new_value)
        self.assertEqual(self.saver.output_file_type, new_value)

    def test_change_wrong_parameter(self):
        with self.assertRaises(Exception):
            self.saver.change_param('not_existing_param', 'new_value')

    def test_get_full_name_wo_pagination(self):
        random_dir = randint(1, 999999)
        random_file_name = randint(1, 999999)
        self.saver.change_param('output_dir', random_dir)
        self.saver.change_param('output_file_name', random_file_name)
        full_filename = self.saver.get_full_filename()
        expected_file_name = f'{random_dir}/{random_file_name}'
        self.assertEqual(full_filename, expected_file_name)

    def test_get_full_name_with_pagination(self):
        random_dir = randint(1, 999999)
        random_file_name = randint(1, 999999)
        self.saver.change_param('output_dir', random_dir)
        self.saver.change_param('output_file_name', random_file_name)
        self.saver.pagination = True
        full_filename = self.saver.get_full_filename()
        expected_file_name = f'{random_dir}/0_{random_file_name}'
        self.assertEqual(full_filename, expected_file_name)


class TestSaverWithCreatingFiles(unittest.TestCase):

    def setUp(self):
        self.saver = Saver()
        self.saver.output_dir = 'test'
        self.saver.output_file_name = 'test'
        self.test_object = [
            {
                'First name': 'Александр',
                'Last name': 'Степанов',
                'Country': 'Россия',
                'City': 'Санкт-Петербург',
                'Birthdate': 'No data',
                'Sex': 'Male'
            }
        ]

    def test_save_with_csv(self):
        self.saver.output_file_type = 'csv'
        self.saver.save(self.test_object)
        saved_data = []
        with open('test/test.csv', 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    saved_data.append(row)
        expected_saved_data = [
            ['First name', 'Last name', 'Country', 'City', 'Birthdate',
             'Sex'],
            ['Александр', 'Степанов', 'Россия', 'Санкт-Петербург',
             'No data', 'Male']
        ]
        self.assertEqual(saved_data, expected_saved_data)

    def test_save_with_tsv(self):
        self.saver.output_file_type = 'tsv'
        self.saver.save(self.test_object)
        saved_data = []
        with open('test/test.tsv', 'r', encoding='utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if row:
                    saved_data.append(row)
        expected_saved_data = [
            ['First name', 'Last name', 'Country', 'City', 'Birthdate',
             'Sex'],
            ['Александр', 'Степанов', 'Россия', 'Санкт-Петербург',
             'No data', 'Male']
        ]
        self.assertEqual(saved_data, expected_saved_data)

    def test_save_with_json(self):
        self.saver.output_file_type = 'json'
        self.saver.save(self.test_object)
        with open('test/test.json', 'r', encoding='utf8') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, self.test_object)

    def tearDown(self):
        rmtree('test')


class TestReportCreator(unittest.TestCase):

    def setUp(self):
        self.vk_api_handler = VkApiHandler()

    def test_create_report_1(self):
        """Case with Pavel Durov"""
        self.vk_api_handler.change_config_param('user_id', 1)
        self.vk_api_handler.change_config_param('users_in_request', 5)
        report = create_report(self.vk_api_handler)
        expected_report = []  # Because Pavel Durov has 0 friend in VK
        self.assertEqual(report, expected_report)

    def test_create_report_2(self):
        """Case with Lindsey Stirling"""
        self.vk_api_handler.change_config_param('user_id', 210700286)
        self.vk_api_handler.change_config_param('users_in_request', 5)
        report = create_report(self.vk_api_handler)
        expected_report = [
            {
                'First name': 'Александр',
                'Last name': 'Степанов',
                'Country': 'Россия',
                'City': 'Санкт-Петербург',
                'Birthdate': 'No data',
                'Sex': 'Male'
            }
        ]
        self.assertEqual(report, expected_report)


if __name__ == '__main__':
    unittest.main()
