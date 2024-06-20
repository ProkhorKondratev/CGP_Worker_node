from pyodm import Node
from app.models import PossibleOptionsModel
import yaml
import os
import aiofiles
import aiofiles.os as aos


class EnumParsingStrategy:
    @staticmethod
    async def parse(name: str, value: str, label: str, **kwargs):
        options = []
        translates = await EnumParsingStrategy.load_translates(name)
        for option in kwargs.get('domain', []):
            option_label = translates.get(option, option)
            options.append(
                {
                    'value': option,
                    'label': option_label,
                }
            )

        return {
            "name": name,
            "label": label,
            "default": value,
            "type": "choice",
            "options": options,
        }

    @staticmethod
    async def load_translates(name: str):
        translations_path = os.path.join(os.path.dirname(__file__), 'translations', 'enums')
        enum_path = os.path.join(translations_path, f'{name}.yaml')

        if not await aos.path.exists(enum_path):
            print(f'ПРЕДУПРЕЖДЕНИЕ: Перевод для enum поля {name} не найден')
            return {}

        async with aiofiles.open(enum_path) as file:
            try:
                content = await file.read()
                return yaml.safe_load(content) or {}
            except yaml.YAMLError as e:
                print(f'Ошибка при загрузке YAML: {e}')
                return {}


class BuiltinsParsingStrategy:
    def __init__(self, type: type) -> None:
        self.type = type

    async def parse(self, name: str, value: str, label: str, **kwargs):
        return {
            "name": name,
            "label": label,
            "default": value == "true" if self.type is bool else self.type(value),
            "type": self.type.__name__,
        }


class ODMParser:
    def __init__(self) -> None:
        self.params_translates = self.load_translates('params')
        self.strategies = {
            "choice": EnumParsingStrategy,
            "int": BuiltinsParsingStrategy(int),
            "float": BuiltinsParsingStrategy(float),
            "string": BuiltinsParsingStrategy(str),
            "bool": BuiltinsParsingStrategy(bool),
        }

    async def get_options(self, node: Node):
        options = node.options()
        fields = []

        for option in options:
            strategy = self.strategies.get(option.type, EnumParsingStrategy)
            label = self.params_translates.get(option.name, {}).get('label', option.name)
            if strategy:
                field_params = await strategy.parse(**vars(option), label=label)
                fields.append(PossibleOptionsModel(**field_params))

        return fields

    def load_translates(self, name: str):
        translations_path = os.path.join(os.path.dirname(__file__), 'translations')

        with open(os.path.join(translations_path, f'{name}.yaml')) as file:
            return yaml.safe_load(file) if file else {}
