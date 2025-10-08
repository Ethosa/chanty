from json import dumps
from typing import Any
import os

from .types.pack_format import PackFormat
from .types.namespace import Namespace
from .types.exceptions import InvalidPackFormat
from .types.position import Position
from .command import CommandBuilder, Selector
from .custom_item import CustomItem
from .types.items import Item
from .types.entity import Entity


class DataPack:
    def __init__(
            self,
            name: str = 'My DataPack',
            description: str = 'My awesome datapack',
            pack_format: PackFormat | int = PackFormat.latest(),
    ):
        self.name: str = name.replace(' ', '_').lower()
        self.description: str = description
        self.namespaces: list[Namespace] = []
        if isinstance(pack_format, PackFormat):
            self.pack_format: int = pack_format.value
        elif isinstance(pack_format, int):
            self.pack_format: int = pack_format
        else:
            raise InvalidPackFormat
    
    def __str__(self) -> str:
        return f'<DataPack "{self.name}" pack_format={self.pack_format}>'

    @property
    def mcmeta(self) -> dict[str, Any]:
        result = {
            'pack': {
                'description': self.description,
                'pack_format': self.pack_format
            }
        }
        return result
    
    def register_namespace(self, namespace: Namespace):
        self.namespaces.append(namespace)
    
    def unregister_namespace(self, namespace: Namespace):
        self.namespaces.remove(namespace)
    
    def _write(self, filename: str, data: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
    
    def export(self, path: str | None = None):
        if path is None:
            path = f'./exported/{self.name}'
        os.makedirs(path, exist_ok=True)
        os.makedirs(f'{path}/data', exist_ok=True)
        os.makedirs(f'{path}/assets', exist_ok=True)

        for namespace in self.namespaces:
            namespace.export(path)

        self._write(f'{path}/pack.mcmeta', dumps(self.mcmeta, indent=2))
