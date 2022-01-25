import json
import logging

import config as default_config


def save_with_json(obj, output_file_name):
    logging.info('Starting saving with json')
    logging.debug(f'Output file: {output_file_name}')
    logging.debug(f'Saved object: {bytes(str(obj), encoding="utf-8")}')
    with open(f'{output_file_name}.json', 'w', encoding='utf8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)
    logging.info('Successfully saved with json')


class Saver:
    save_funcs = {
        'json': save_with_json,
    }

    @staticmethod
    def print_supported_types():
        print('Supported file types:')
        for type in Saver.save_funcs:
            print(type)

    def __init__(self):
        self.output_dir = default_config.default_directory
        self.output_file_name = default_config.default_output_file_name
        self.output_file_type = default_config.default_output_file_type
        logging.debug('Saver initialised')

    def change_param(self, param_name, new_value):
        logging.info(f'Saver changing {param_name} with {new_value}')
        if param_name == 'output_dir':
            self.output_dir = new_value
        elif param_name == 'output_file_name':
            self.output_file_name = new_value
        elif param_name == 'output_file_type':
            self.output_file_type = new_value
        else:
            raise Exception(f"No parameter with name {param_name}")

    def get_full_filename(self, prefix=''):
        logging.debug(f'Saver returning filename with prefix {prefix}')
        if not self.output_dir.endswith('/'):  # Adding slash in the end of
            self.output_dir += '/'             # output directory if needed
        prefix = str(prefix)  # in case if prefix is int
        if len(prefix) > 0:
            prefix += '_'  # Underscore for divide prefix from filename
        output_file = f'{self.output_dir}{prefix}{self.output_file_name}'
        return output_file

    def save(self, obj, prefix=''):
        output_file = self.get_full_filename(prefix)
        logging.info(f'Saver started to saving object in file {output_file}')
        logging.info(f'File type is {self.output_file_type}')
        logging.debug(f'Saved object: {bytes(str(obj), encoding="utf-8")}')
        if self.output_file_type in Saver.save_funcs:
            Saver.save_funcs[self.output_file_type](obj, output_file)
        else:
            raise Exception("File type is not supported")
