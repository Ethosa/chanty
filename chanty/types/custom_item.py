from __future__ import annotations
from typing import Callable, Any
from json import dumps

from .items import Item
from .custom_model import CustomModel

from .translations import Translations


class CustomItem:
    _CUSTOM_ITEM_INDEX: int = 0
    def __init__(
            self,
            item: str | Item,
            nbt: dict | None = None,
            custom_item_index: int | str | None = None
    ):
        if nbt is None:
            nbt = {}

        self.item = item
        self._namespace = 'minecraft'
        self.nbt = nbt
        self._callback_index = 0

        if custom_item_index is None:
            self._index = CustomItem._CUSTOM_ITEM_INDEX
            self.nbt['minecraft:custom_data'] = {'custom_item_index': str(CustomItem._CUSTOM_ITEM_INDEX)}
            CustomItem._CUSTOM_ITEM_INDEX += 1
        else:
            self._index = custom_item_index
            self.nbt['minecraft:custom_data'] = {'custom_item_index': str(custom_item_index)}

        self._advancements = []
        self._handlers = []
        self._registries = []
    
    def __setitem__(self, key: str, value: Any):
        self.nbt[key] = value
    
    def __getitem__(self, key: str):
        return self.nbt[key]
    
    def __delitem__(self, key: str):
        del self.nbt[key]
    
    def set_name(self, name: str | dict[str, Any]) -> CustomItem:
        if isinstance(name, str):
            if Translations.has_key(name):
                self.nbt['minecraft:custom_name'] = {"translate": Translations.get_str(name), "italic": False}
            else:
                self.nbt['minecraft:custom_name'] = {"text": name, "italic": False}
        else:
            self.nbt['minecraft:custom_name'] = name
        return self

    def set_lore(self, *lines: str) -> CustomItem:
        lore = [
            {
                "translate": Translations.get_str(line),
                "color": "gray",
                "italic": False
            } if Translations.has_key(line) else {
                "text": line,
                "color": "gray",
                "italic": False
            } if isinstance(line, str) else line
            for line in lines
        ]
        self.nbt['minecraft:lore'] = lore
        return self
    
    def glint(self, enabled: bool = True) -> CustomItem:
        if enabled:
            self.nbt["minecraft:enchantment_glint_override"] = True
        else:
            self.nbt.pop("minecraft:enchantment_glint_override", None)
        return self
    
    def consumable(self, consumable_seconds: int| None = None) -> CustomItem:
        self['minecraft:consumable'] = {}
        if consumable_seconds is not None:
            self['minecraft:consumable']['consume_seconds'] = consumable_seconds
        return self

    def set_model(self, model: str | CustomModel) -> CustomItem:
        self.nbt["minecraft:item_model"] = str(model)
        return self
    
    def on_right_click(self, func: Callable[[], str]):
        def decorator():
            id = f'on_custom_item_{self._index}_{self._callback_index}_right_click'
            self._callback_index += 1
            self._advancements.append({
                'id': id,
                'adv': {
                    'criteria': {
                        'requirement': {
                            'trigger': 'minecraft:consume_item',
                            'conditions': {
                                'item': {
                                    'items': [self.item],
                                    'components': self.nbt
                                }
                            }
                        }
                    },
                    'rewards': {
                        'function': f'{self._namespace}:{id}'
                    }
                }
            })
            self['minecraft:consumable'] = {
                'consume_seconds': 0,
                'has_consume_particles': False,
                'sound': {'sound_id': ''},
                'animation': 'none',
            }
            self._handlers.append({
                'func_name': id,
                'action': 'on_right_click',
                'code': (
                    f'advancement revoke @s only {self._namespace}:{id}'
                    '\n' + func()
                ) 
            })
        self._registries.append(decorator)
    
    def __str__(self) -> str:
        nbt = ','.join([f'{key}={dumps(val)}' for key, val in self.nbt.items()])
        return f'{str(self.item)}[{nbt}]'
