from typing import Callable
from json import dumps

from .types.items import Item


_CUSTOM_ITEM_INDEX = 0


class CustomItem:
    def __init__(
            self,
            item: str | Item,
            nbt: dict = {}
    ):
        global _CUSTOM_ITEM_INDEX
        self.item = item
        self._namespace = 'minecraft'
        self._index = _CUSTOM_ITEM_INDEX
        self.nbt = nbt
        self.nbt['minecraft:custom_data'] = {'custom_item_index': _CUSTOM_ITEM_INDEX}
        _CUSTOM_ITEM_INDEX += 1

        self._advancements = []
        self._handlers = {}
        self._registries = []
    
    def __setitem__(self, key, value):
        self.nbt[key] = value
    
    def __getitem__(self, key):
        return self.nbt[key]
    
    def __delitem__(self, key):
        del self.nbt[key]
    
    def consumable(self, consumable_seconds: int| None = None) -> 'CustomItem':
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
                                    'items': [str(self.item)],
                                    'nbt': '{custom_data:' + dumps(self.nbt["minecraft:custom_data"]) + '}',
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
