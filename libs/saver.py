import csv
import json
import logging
import os

import config as default_config


def create_new_csv(obj, file_name):
    logging.info('Creating new csv')
    logging.debug(f'Creating file: {file_name}.csv')
    with open(f'{file_name}.csv', 'w', encoding='utf8') as f:
        fieldnames = list(obj[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    logging.info(f'Successfully create {file_name}.csv')


def create_new_tsv(obj, file_name):
    logging.info('Creating new tsv')
    logging.debug(f'Creating file: {file_name}.tsv')
    with open(f'{file_name}.tsv', 'w', encoding='utf8') as f:
        fieldnames = list(obj[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames,
                                delimiter='\t')
        writer.writeheader()
    logging.info(f'Successfully create {file_name}.tsv')


def create_new_json(obj, file_name):
    # Json doesn't need set headings, so we just dump empty array
    logging.info('Creating new json')
    logging.debug(f'Creating file: {file_name}.json')
    with open(f'{file_name}.json', 'w', encoding='utf8') as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    logging.info(f'Successfully create {file_name}.json')


def append_with_csv(obj, file_name):
    logging.info('Appending with csv')
    logging.debug(f'Appending file: {file_name}')
    logging.debug(f'Saved object: {bytes(str(obj), encoding="utf-8")}')
    with open(f'{file_name}.csv', 'a', encoding='utf8') as f:
        fieldnames = list(obj[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for friend in obj:
            writer.writerow(friend)
    logging.info('Successfully appended with csv')


def append_with_tsv(obj, file_name):
    logging.info('Appending with tsv')
    logging.debug(f'Appending file: {file_name}')
    logging.debug(f'Saved object: {bytes(str(obj), encoding="utf-8")}')
    with open(f'{file_name}.tsv', 'a', encoding='utf8') as f:
        fieldnames = list(obj[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames,
                                delimiter='\t')
        for friend in obj:
            writer.writerow(friend)
    logging.info('Successfully appended with tsv')


def append_with_json(obj, file_name):
    with open(f'{file_name}.json', 'r', encoding='utf8') as f:
        old_data = json.load(f)
    updated_data = old_data + obj  # concatenation of lists
    with open(f'{file_name}.json', 'w', encoding='utf8') as f:
        json.dump(updated_data, f, ensure_ascii=False)


class Saver:
    """
    This class is responsible for saving data

    How to use:
    1. Change config values if you need: output_dir, output_file_name,
    output_file_type, users_in_file, pagination.
    You can do it using saver_instance.change_param method.
    2. Run saver_instance.save(object_to_save)

    To add other data types support, just add function of creating
    file and function of appending data to create_new_file_funcs
    and append_funcs dictionaries (look below).

    Saving object example:
    [
        {
            "First name": "Akio",
            "Last name": "Switch",
            "Country": "Россия",
            "City": "Москва",
            "Birthdate": "No data",
            "Sex": "Male"
        },
        ...
    ]
    """
    # This functions creates new file and set up headings if needed.
    # They takes object and output_file_name (object needed for
    # headings set up)
    create_new_file_funcs = {
        'csv': create_new_csv,
        'tsv': create_new_tsv,
        'json': create_new_json,
    }
    # This functions appends object into existing file
    append_funcs = {
        'csv': append_with_csv,
        'tsv': append_with_tsv,
        'json': append_with_json,
    }

    @staticmethod
    def print_supported_types():
        print('''\n
        Supported file types: ''', end='')
        for file_type in Saver.append_funcs:
            print(file_type, end=', ')
        print('\n')

    def __init__(self):
        self.output_dir = default_config.default_directory
        self.output_file_name = default_config.default_output_file_name
        self.output_file_type = default_config.default_output_file_type
        self.users_in_file = default_config.default_users_in_file
        self.pagination = default_config.default_pagination
        self.users_in_current_file = 0
        self.file_prefix = 0
        logging.debug('Saver initialised')

    def save(self, obj):
        self.__create_output_dir_if_needed()
        output_file = self.get_full_filename()
        saved_friends = 0
        if self.file_prefix == 0:  # Creating first file
            self.create_new_file(obj)
        # If pagination is False, then file can contain unlimited amount
        # of users
        if not self.pagination:
            self.users_in_file = 99999999999
        logging.info(f'Saver started to saving object in file '
                     f'{output_file}')
        logging.info(f'File type is {self.output_file_type}')
        logging.debug(f'Saved object: '
                      f'{bytes(str(obj), encoding="utf-8")}')
        while saved_friends < len(obj):
            if self.users_in_current_file >= self.users_in_file:
                self.create_new_file(obj)
            # Amount of people we can add:
            free_place_in_file = self.users_in_file - \
                                 self.users_in_current_file
            logging.debug(f'Free place in file {free_place_in_file}')
            appending_friends = obj[saved_friends: saved_friends +
                                                   free_place_in_file]
            self.append_to_file(appending_friends)
            saved_friends += len(appending_friends)
            logging.debug(f'Saved friends {saved_friends} from saver')

    def change_output_file_type(self, new_value):
        if new_value in Saver.append_funcs:
            self.output_file_type = new_value
        else:
            raise WrongParameterValueError

    def change_param(self, param_name, new_value):
        logging.info(f'Saver changing {param_name} with {new_value}')
        if param_name == 'output_dir':
            self.output_dir = str(new_value)
        elif param_name == 'output_file_name':
            self.output_file_name = str(new_value)
        elif param_name == 'output_file_type':
            self.change_output_file_type(new_value)
        elif param_name == 'users_in_file':
            try:
                if int(new_value) <= 0:
                    raise ValueError
                self.users_in_file = int(new_value)
            except ValueError:
                raise WrongParameterValueError
        elif param_name == 'pagination':
            self.pagination = not self.pagination
        else:
            raise Exception(f'No parameter with name {param_name}')

    def get_full_filename(self):
        """Returning full file path from current directory"""
        logging.debug(f'Saver returning filename with prefix '
                      f'{self.file_prefix}')
        # Add slash in the end of output_dir if output_dir is exist
        # and not ending with slash
        if self.output_dir and not self.output_dir.endswith('/'):
            self.output_dir += '/'
        # Adding prefix if pagination is True
        prefix = ''
        if self.pagination:
            prefix = f'{self.file_prefix}_'  # in case if prefix is int
        output_file = f'{self.output_dir}{prefix}{self.output_file_name}'
        return output_file

    def __create_output_dir_if_needed(self):
        if not os.path.exists(self.output_dir) and self.output_dir:
            os.makedirs(self.output_dir)

    def create_new_file(self, obj):
        self.file_prefix += 1
        file_name = self.get_full_filename()
        Saver.create_new_file_funcs[self.output_file_type](obj,
                                                           file_name)
        self.users_in_current_file = 0

    def append_to_file(self, obj):
        file_name = self.get_full_filename()
        Saver.append_funcs[self.output_file_type](obj, file_name)
        self.users_in_current_file += len(obj)


class WrongParameterValueError(Exception):
    def __init__(self, value='Wrong parameter given'):
        self.value = value

    def __str__(self):
        return repr(self.value)
