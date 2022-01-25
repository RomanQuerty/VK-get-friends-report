import os
from saver import Saver
from vk_api_handler import VkApiHandler
import report_creator
import logging


# It's 'clear' command for terminal (should work in linux and windows)
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def handle_command(commands_dict):
    logging.info('Handling command')
    logging.info(commands_dict.keys())
    input_command = input()
    logging.info(f'Inputted command: {input_command}')
    if input_command in commands_dict:
        commands_dict[input_command]()
    elif 'default' in commands_dict:
        commands_dict['default']()
    else:
        raise Exception(f'Wrong command and no default command\n{commands_dict.keys()}')


class ConsoleApp:
    """
    This class is responsible for user interface and instance config
    params
    """
    def __init__(self):
        self.vk_api_handler = VkApiHandler()
        self.saver = Saver()
        logging.debug("ConsoleApp initialised")

    def main_screen(self, message=''):
        logging.info(f'Showing main_screen with message "{message}"')
        cls()
        print(f'''
        Hello!
        It's "VK get friends report" app by Maxim Novoselsky.
        
        Current configuration:
        Access token: {self.vk_api_handler.config['access_token']}
        User ID: {self.vk_api_handler.config['user_id']}
        Output file: {self.saver.get_full_filename()}.{self.saver.output_file_type}
        Amount of users in single file: {self.vk_api_handler.config['users_in_request']}
        
        Please enter:
        1 - Get report
        2 - Change configuration
        3 - Exit
        
        {message}
        ''')

        commands_dict = {
            '1': self.save_report,
            '2': self.change_configuration_screen,
            '3': self.exit,
            'default': lambda: self.main_screen('Wrong command'),
        }

        handle_command(commands_dict)

    def save_report(self):
        report_creator.create_and_save_report(self.vk_api_handler, self.saver)
        self.exit()

    def change_config_parameter(self, param_name):
        logging.info(f'Changing parameter "{param_name}"')
        print(f'''
        You going to change {param_name}.
        
        Please, enter new value.
        ''')
        new_value = input()
        # We have different config params in vk_api_handler and in saver
        # so we need to choose which parameter we want to change.
        # It's easiest but, probably, not the best way how to choose:
        # If parameter not in vk_api handler then it in saver.
        if param_name in self.vk_api_handler.config:
            self.vk_api_handler.change_config_param(param_name, new_value)
        else:
            self.saver.change_param(param_name, new_value)
        self.change_configuration_screen(f'{param_name} successfully changed')

    def change_configuration_screen(self, message=''):
        logging.info(f'Showing change_configuration_screen with message "{message}"')
        cls()
        print(f'''
        Current configuration:
        Access token: {self.vk_api_handler.config['access_token']}
        User ID: {self.vk_api_handler.config['user_id']}
        Output file: {self.saver.get_full_filename()}.{self.saver.output_file_type}
        Amount of users in single file: {self.vk_api_handler.config['users_in_request']}
        
        {message}
        
        What do you want to change?
        1 - Access token
        2 - User ID
        3 - Output file directory
        4 - Output file name
        5 - Output file type
        6 - Amount of users in single file
        7 - Get Report
        8 - Exit
        ''')

        commands_dict = {
            '1': lambda: self.change_config_parameter('access_token'),
            '2': lambda: self.change_config_parameter('user_id'),
            '3': lambda: self.change_config_parameter('output_dir'),
            '4': lambda: self.change_config_parameter('output_file_name'),
            '5': lambda: self.change_config_parameter('output_file_type'),
            '6': lambda: self.change_config_parameter('users_in_request'),
            '7': self.save_report,
            '8': self.exit,
            'default': lambda: self.change_configuration_screen('Wrong command'),
        }

        handle_command(commands_dict)

    @staticmethod
    def exit():
        logging.info('Exiting')
        print("\nGoodbye!")
