import os
from json import dumps, loads, JSONDecodeError
from typing import Callable

from .recipe import Recipe
from .custom_item import CustomItem
from ..command.builder import CommandBuilder
from ..logging import error, debug, info


class Namespace:
    def __init__(self, name: str):
        self.name = name.replace(' ', '_').lower()
        self.advancements = []
        self.dimension = []
        self.dimension_type = []
        self.functions: dict[str, Callable[[], str]] = {}
        self.loot_tables = []
        self.predicates = {}
        self.recipes: list[Recipe] = []
        self.structures = []
        self.tags = []
        self.chat_type = []
        self.damage_type = []
        self.worldgen = None

        self._custom_items = []

        self._on_load_handler: Callable[[], str] | None = None
        self._every_tick_handler: Callable[[], str] | None = None
    
    def on_load(self, func: Callable[[], str]):
        """
        Registers mcfunction for `load` event
        """
        info(f'{self.name}: register {func.__name__}@on_load')
        self._on_load_handler = func
        return func

    def every_tick(self, func: Callable[[], str]):
        """
        Registers mcfunction for `tick` event
        """
        info(f'{self.name}: register {func.__name__}@every_tick')
        self._every_tick_handler = func
        return func

    def function(self, func_or_name: Callable[[], str] | str):
        """
        Registers mcfunction to use it later
        """
        if isinstance(func_or_name, str):
            def decorator(func: Callable[[], str]):
                func.id = f'{self.name}:{func_or_name}'
                info(f'{self.name}: register {func_or_name}.mcfunction')
                self.functions[func_or_name] = func
                return func
            return decorator
        else:
            func_or_name.id = f'{self.name}:{func_or_name.__name__}'
            self.functions[func_or_name.__name__] = func_or_name
            info(f'{self.name}: register {func_or_name.__name__}.mcfunction')
            return func_or_name

    def register(self, data: CustomItem | Recipe):
        """
        Registers custom item
        """
        if isinstance(data, CustomItem):
            data._namespace = self.name
            self._custom_items.append(data)
        elif isinstance(data, Recipe):
            self.recipes.append(data)
    
    def _write(self, filename: str, data: str | CommandBuilder):
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(data, CommandBuilder):
                f.write(data.build())
            else:
                f.write(data)

    def _append_tag(self, tag_path: str, value: str):
        if os.path.exists(tag_path):
            with open(tag_path, 'r', encoding='utf-8') as f:
                try:
                    tag_data = loads(f.read())
                except JSONDecodeError:
                    tag_data = {"values": []}
        else:
            tag_data = {"values": []}

        if value not in tag_data["values"]:
            tag_data["values"].append(value)

        self._write(tag_path, dumps(tag_data, indent=2))
    
    def export(self, path: str):
        """
        Builds sources and creates folders with subfolders into datapack destionation.
        """
        info(f'{self.name}: make folders')
        namespace_path = f'{path}/data/{self.name}'
        os.makedirs(f'{namespace_path}/recipe', exist_ok=True)
        os.makedirs(f'{namespace_path}/function', exist_ok=True)
        os.makedirs(f'{namespace_path}/predicate', exist_ok=True)
        os.makedirs(f'{namespace_path}/advancement', exist_ok=True)
        
        # CUSTOM ITEMS
        for item in self._custom_items:
            info(f'{self.name}: register CustomItem(#{item._index}, "{item.item}")')
            for registry in item._registries:
                registry()
            for adv in item._advancements:
                self._write(
                    f'{namespace_path}/advancement/{adv["id"]}.json',
                    dumps(adv["adv"], indent=2)
                )
            for handler in item._handlers:
                self._write(
                    f'{namespace_path}/function/{handler["func_name"]}.mcfunction',
                    handler["code"]
                )
        
        # FUNCTIONS
        for key, func in self.functions.items():
            info(f'{self.name}: register function("{key}.mcfunction")')
            self._write(f"{namespace_path}/function/{key}.mcfunction", func())
        
        # RECIPES
        for recipe in self.recipes:
            info(f'{self.name}: register recipe("{recipe.id}.json")')
            self._write(f'{namespace_path}/recipe/{recipe.id}.json', dumps(recipe.to_json(), indent=2))
        
        # load/tick HANDLERS
        tags_path = f"{path}/data/minecraft/tags/function"
        os.makedirs(tags_path, exist_ok=True)
        if self._on_load_handler:
            self._write(
                f"{namespace_path}/function/load.mcfunction",
                self._on_load_handler()
            )
            self._append_tag(f"{tags_path}/load.json", f"{self.name}:load")
        if self._every_tick_handler:
            self._write(
                f"{namespace_path}/function/tick.mcfunction",
                self._every_tick_handler()
            )
            self._append_tag(f"{tags_path}/tick.json", f"{self.name}:tick")
