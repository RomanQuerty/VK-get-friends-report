import requests
import config as default_config
import logging


def raise_exception_if_vk_response_is_error(response):
    logging.debug(f'Response got:')
    logging.debug(response.content)
    if 'error' in response.text:
        raise Exception(f"VK responded with error\n{response.text}")


class VkApiHandler:
    def __init__(self):
        # default config
        self.config = {
            'access_token': default_config.default_access_token,
            'user_id': default_config.default_user_id,
            'users_in_request': default_config.default_users_in_file,
        }
        logging.debug("VkApiHandler initialised")

    def change_config_param(self, param_name, new_value):
        self.config[param_name] = new_value
        logging.info(f'VkApiHandler changed {param_name} with '
                     f'{new_value}')

    def run_VK_method(self, method_name, params_dict):
        logging.debug(f'Running VK method {method_name}')
        url = f'https://api.vk.com/method/{method_name}'
        params_dict['v'] = '5.131'
        params_dict['access_token'] = self.config['access_token']
        try:
            response = requests.get(url, params=params_dict)
        except requests.exceptions.ConnectionError:
            raise Exception(f'Connection error. Check URL and internet '
                            f'connection:\n{url}')
        raise_exception_if_vk_response_is_error(response)  # It also log
        return response

    def get_friends_amount(self):
        # https://dev.vk.com/method/friends.get
        logging.info('Getting friends amount')
        params = {
            "user_id": self.config['user_id'],
            "count": 1,
            "offset": 0,
            "order": "name",
            "fields": ''
        }
        response = self.run_VK_method('friends.get', params).json()
        return response['response']['count']

    def __get_friends_raw_data(self, offset=0):
        # https://dev.vk.com/method/friends.get
        params = {
            "user_id": self.config['user_id'],
            "count": self.config['users_in_request'],
            "offset": offset,
            "order": "name",
            "fields": 'country,city,bdate,sex'
        }
        response = self.run_VK_method('friends.get', params).json()
        friends_data = response['response']['items']
        return friends_data

    def get_friends_data_list(self, offset=0):
        """
        This method gets raw VK data and changes it according report
        structure (skipping deleted and banned accounts).
        e.g. raw vk friends data:
            {
                "response":{
                "count":1175
                "items":[
                    0:{
                    "id":126026250
                    "deactivated":"banned"
                    "first_name":"Πавел"
                    "last_name":"Μаксимов"
                    "track_code":"4be6a67e6sLKi..."
                    }
                    1:{
                    "id":106503332
                    "first_name":"Akio"
                    "last_name":"Switch"
                    "can_access_closed":false
                    "is_closed":true
                    "track_code":"e072771fcSu3l..."
                    }
                ]
            }
        processed friends data:
        [
            {
                "First name": "Akio",
                "Last name": "Switch",
                "Country": "Россия",
                "City": "Москва",
                "Birthdate": "Нет данных",
                "Sex": "Male"
            }
        ]
        """
        # This function contains pretty big if/else construction,
        # but I think it is still more understandable and easy to
        # change, then using lot of different functions for each case.
        # BTW, we can't create universal "set_value" function, because
        # values are too different (e.g. look at city, bdate and sex).
        raw_friends_data = self.__get_friends_raw_data(offset)
        processed_friends_list = []
        for raw_friend_data in raw_friends_data:
            # We skip deleted and deactivated users
            if raw_friend_data['first_name'] == 'DELETED' or \
                    'deactivated' in raw_friend_data:
                continue
            processed_friend_data = {
                'First name': raw_friend_data['first_name'],
                'Last name': raw_friend_data['last_name']
            }
            # Default country, city, bdate, sex value
            country = city = bdate = sex = 'Нет данных'
            # Country
            if 'country' in raw_friend_data:
                country = raw_friend_data['country']['title']
            processed_friend_data['Country'] = country
            # City
            if 'city' in raw_friend_data:
                city = raw_friend_data['city']['title']
            processed_friend_data['City'] = city
            # Birthdate
            if 'bdate' in raw_friend_data:
                bdate = raw_friend_data['bdate'].replace('.', '-')
            processed_friend_data['Birthdate'] = bdate
            # Sex
            if 'sex' in raw_friend_data:
                if raw_friend_data['sex'] == 1:
                    sex = 'Female'
                elif raw_friend_data['sex'] == 2:
                    sex = 'Male'
                else:
                    sex = 'Any'
            processed_friend_data['Sex'] = sex
            processed_friends_list.append(processed_friend_data)
        return processed_friends_list
