from pyodm import Node
from models import OptionsModel
import yaml
import os


class ODMParser:
    def __init__(self) -> None:
        self.params_translates = self.load_translates('params')

    def get_options(self, node: Node):
        options = node.options()

        for option in options:
            print('---')
            print('NAME:', option.name)
            print('LABEL:', self.params_translates[option.name].get('label', option.name))
            print('DEFAULT:', option.value, type(option.value))
            print('TYPE:', option.type)
            # print(option.help)
            print(option.domain, type(option.domain))
            print('---')

        return True

    def load_translates(self, name: str):
        translations_path = os.path.join(os.path.dirname(__file__), 'translations')

        with open(os.path.join(translations_path, f'{name}.yaml')) as file:
            return yaml.safe_load(file)
