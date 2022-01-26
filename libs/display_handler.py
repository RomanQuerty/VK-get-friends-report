import os
from .saver import Saver, WrongParameterValueError
from .vk_api_handler import VkApiHandler
from libs import report_creator
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
        logging.debug('ConsoleApp initialised')

    def __print_configuration(self):
        print(f'''
        Current configuration:
        Access token: {self.vk_api_handler.config['access_token']}
        User ID: {self.vk_api_handler.config['user_id']}
        Output file: {self.saver.get_full_filename()}.{self.saver.
              output_file_type}
        Amount of users in request: {self.vk_api_handler.config['users_in_request']}
        Amount of users in file: {self.saver.users_in_file} (works only if pagination is on)
        Pagination: {self.saver.pagination}\n''')

    def main_screen(self, message=''):
        logging.info(f'Showing main_screen with message "{message}"')
        cls()
        print(f'''
        Hello!
        It's "VK get friends report" app by Maxim Novoselsky.
        ''')

        self.__print_configuration()

        print(f'''
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
        report_creator.create_and_save_reports(self.vk_api_handler,
                                               self.saver)
        self.exit()

    def change_config_parameter(self, param_name):
        """The way how I change parameters are a little bit clumsy, but
        refactoring all of parameters will take too much time. I suppose
        there is no so much additional parameters we can add in this
        system, so you probable will never change this part of code. But
        if you suddenly will, you better should refactor it.
        """
        logging.info(f'Changing parameter "{param_name}"')
        print(f'''
        You going to change {param_name}.
        
        Please, enter new value.
        If you changed your mind just press enter.
        ''')
        if param_name == 'output_file_type':
            Saver.print_supported_types()
        # If param_name is pagination we will just reverse it (True to
        # False, or backward) without asking new_value
        if param_name == 'pagination':
            self.saver.change_param(param_name, '')
            self.change_configuration_screen(f'{param_name} '
                                             f'successfully changed')
            return
        new_value = input()
        if new_value == '':
            self.change_configuration_screen(f'Nothing was changed')
            return
        # We have different config params in vk_api_handler and in saver
        # so we need to choose which parameter we want to change.
        # It's easiest but, probably, not the best way how to choose:
        # If parameter not in vk_api handler then it in saver.
        try:
            if param_name in self.vk_api_handler.config:
                self.vk_api_handler.change_config_param(param_name, new_value)
            else:
                self.saver.change_param(param_name, new_value)
        except WrongParameterValueError:
            self.change_configuration_screen(f'Wrong parameter value. '
                                             f'Parameter has not been '
                                             f'changed.')
        else:
            self.change_configuration_screen(f'{param_name} '
                                             f'successfully changed')

    def change_configuration_screen(self, message=''):
        logging.info(f'Showing change_configuration_screen with message "{message}"')
        cls()
        self.__print_configuration()
        print(f'''
        What do you want to change?
        1 - Access token
        2 - User ID
        3 - Output file directory
        4 - Output file name
        5 - Output file type
        6 - Amount of users in request
        7 - Amount of users in single file
        8 - Pagination
        ------------------------------
        9 - Get Report
        10 - Exit
        
        {message}
        ''')

        commands_dict = {
            '1': lambda: self.change_config_parameter('access_token'),
            '2': lambda: self.change_config_parameter('user_id'),
            '3': lambda: self.change_config_parameter('output_dir'),
            '4': lambda: self.change_config_parameter('output_file_name'),
            '5': lambda: self.change_config_parameter('output_file_type'),
            '6': lambda: self.change_config_parameter('users_in_request'),
            '7': lambda: self.change_config_parameter('users_in_file'),
            '8': lambda: self.change_config_parameter('pagination'),
            '9': self.save_report,
            '10': self.exit,
            'default': lambda: self.change_configuration_screen('Wrong command'),
        }

        handle_command(commands_dict)

    @staticmethod
    def exit():
        logging.info('Exiting')
        print("\nGoodbye!")
