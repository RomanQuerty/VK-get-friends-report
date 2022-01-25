import requests
import config as default_config


class VkApiHandler:
    def __init__(self):
        # default config
        self.config = {
            'access_token': default_config.default_access_token,
            'user_id': default_config.default_user_id,
            'users_in_file': default_config.default_users_in_file,
        }

    def change_config_param(self, param_name, new_value):
        self.config[param_name] = new_value

    def run_VK_method(self, method_name, params_dict):
        url = f'https://api.vk.com/method/{method_name}'
        params_dict['v'] = '5.131'
        params_dict['access_token'] = self.config['access_token']
        response = requests.get(url, params=params_dict)
        return response

    def get_friends_amount(self):
        params = {
            "user_id": self.config['user_id'],
            "count": 1,
            "offset": 0,
            "order": "name",
            "fields": ''
        }
        response = self.run_VK_method('friends.get', params).json()
        return response['response']['count']

    def get_friends_raw_data(self, offset=0):
        params = {
            "user_id": self.config['user_id'],
            "count": self.config['users_in_file'],
            "offset": offset,
            "order": "name",
            "fields": 'country,city,bdate,sex'
        }
        response = self.run_VK_method('friends.get', params).json()
        friends_data = response['response']['items']
        return friends_data

    def get_friends_data_list(self, offset=0):
        # This function contains pretty big if/else construction,
        # but I think it is still more understandable and easier to
        # change, then using lot of different functions for each case.
        # BTW, we can't create universal "set_value" function, because
        # values are too different (e.g. look at city, bdate and sex).
        raw_friends_data = self.get_friends_raw_data(offset)
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
