import json
import config as default_config


def save_with_json(obj, output_file_name):
    with open(f'{output_file_name}.json', 'w', encoding='utf8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)


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

    def change_param(self, param_name, new_value):
        if param_name == 'output_dir':
            self.output_dir = new_value
        elif param_name == 'output_file_name':
            self.output_file_name = new_value
        elif param_name == 'output_file_type':
            self.output_file_type = new_value
        else:
            raise Exception(f"No parameter with name {param_name}")

    def get_full_filename(self, prefix=''):
        if not self.output_dir.endswith('/'):  # Adding slash in the end of
            self.output_dir += '/'             # output directory if needed
        prefix = str(prefix)  # in case if prefix is int
        if len(prefix) > 0:
            prefix += '_'  # Underscore for divide prefix from filename
        output_file = f'{self.output_dir}{prefix}{self.output_file_name}'
        return output_file

    def save(self, obj, prefix=''):
        output_file = self.get_full_filename(prefix)
        if self.output_file_type in Saver.save_funcs:
            Saver.save_funcs[self.output_file_type](obj, output_file)
        else:
            raise Exception("File type is not supported")
