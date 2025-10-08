from __future__ import annotations
from typing import Callable, Any
from json import dumps

from .types.items import Item


_CUSTOM_ITEM_INDEX = 0


class CustomItem:
    def __init__(
            self,
            item: str | Item,
            nbt: dict = {},
            custom_item_index: int | str | None = None
    ):
        global _CUSTOM_ITEM_INDEX
        self.item = item
        self._namespace = 'minecraft'
        self.nbt = nbt
        if custom_item_index is None:
            self._index = _CUSTOM_ITEM_INDEX
            self.nbt['minecraft:custom_data'] = {'custom_item_index': _CUSTOM_ITEM_INDEX}
            _CUSTOM_ITEM_INDEX += 1
        else:
            self._index = custom_item_index
            self.nbt['minecraft:custom_data'] = {'custom_item_index': custom_item_index}

        self._advancements = []
        self._handlers = {}
        self._registries = []
    
    def __setitem__(self, key, value):
        self.nbt[key] = value
    
    def __getitem__(self, key):
        return self.nbt[key]
    
    def __delitem__(self, key):
        del self.nbt[key]
    
    def set_name(self, name: str | dict[str, Any]) -> CustomItem:
        if isinstance(name, str):
            self.nbt['minecraft:custom_name'] = {"text": name, "italic": False}
        else:
            self.nbt['minecraft:custom_name'] = name
        return self

    def set_lore(self, *lines: str) -> CustomItem:
        lore = [
            {"text": line, "color": "gray", "italic": False} if isinstance(line, str) else line
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
    
    def on_right_click(self, func: Callable[[], str]):
        def decorator():
            id = f'on_custom_item_{self._index}_right_click'
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
            if 'on_right_click' not in self._handlers:
                self._handlers['on_right_click'] = []
            self._handlers['on_right_click'].append({
                'func_name': id,
                'code': f'advancement revoke @s only {self._namespace}:{id}' + '\n' + func() 
            })
        self._registries.append(decorator)
    
    def __str__(self) -> str:
        nbt = ','.join([f'{key}={dumps(val)}' for key, val in self.nbt.items()])
        return f'{str(self.item)}[{nbt}]'
