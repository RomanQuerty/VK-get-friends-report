import requests
import config as default_config
import logging
from .saver import WrongParameterValueError


def raise_exception_if_vk_response_is_error(response):
    logging.debug(f'Response got:')
    logging.debug(response.content)
    if 'error' in response.text:
        error_info = response.json()['error']
        raise Exception(f'VK responded with error\n'
                        f'Error code: {error_info["error_code"]}\n'
                        f'Error message: {error_info["error_msg"]}\n'
                        f'Requested params: '
                        f'{error_info["request_params"]}')


class VkApiHandler:
    def __init__(self):
        # default config
        self.config = {
            'access_token': default_config.default_access_token,
            'user_id': default_config.default_user_id,
            'users_in_request': default_config.default_users_in_request,
        }
        logging.debug("VkApiHandler initialised")

    def change_config_param(self, param_name, new_value):
        if param_name == 'users_in_request':
            try:
                if int(new_value) <= 0:
                    raise ValueError
                new_value = int(new_value)
            except ValueError:
                raise WrongParameterValueError
        self.config[param_name] = new_value
        logging.info(f'VkApiHandler changed {param_name} with '
                     f'{new_value}')

    def get_VK_method_response(self, method_name, params_dict):
        logging.debug(f'Running VK method {method_name}')
        url = f'https://api.vk.com/method/{method_name}'
        params_dict['v'] = '5.131'
        params_dict['access_token'] = self.config['access_token']
        try:
            response = requests.get(url, params=params_dict)
        except requests.exceptions.ConnectionError:
            raise Exception(f'Connection error. Check URL and internet '
                            f'connection:\n{url}')
        # even if exception doesnt raised, response will be logged
        raise_exception_if_vk_response_is_error(response)
        return response

    def get_friends_amount(self):
        # https://dev.vk.com/method/friends.get
        logging.info('Getting friends amount')
        params = {
            'user_id': self.config['user_id'],
            'count': 1,
            'offset': 0,
            'order': 'name',
            'fields': ''  # without fields we will get only friends
        }                 # amount in response
        response = self.get_VK_method_response('friends.get', params)
        response = response.json()
        return response['response']['count']

    def get_friends_data(self, offset=0):
        # See list of possible params here:
        # https://dev.vk.com/method/friends.get
        params = {
            'user_id': self.config['user_id'],
            'count': self.config['users_in_request'],
            'offset': offset,
            'order': 'name',
            'fields': 'country,city,bdate,sex'
        }
        response = self.get_VK_method_response('friends.get', params)
        response = response.json()
        friends_data = response['response']['items']
        return friends_data
