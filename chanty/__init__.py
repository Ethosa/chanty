from json import dumps
from typing import Any
import os
import io
import shutil

import zipfile

from .types.pack_format import PackFormat
from .types.namespace import Namespace
from .types.exceptions import InvalidPackFormat
from .types.position import Position
from .command import CommandBuilder, Selector, Random
from .types.custom_item import CustomItem
from .types.custom_model import CustomModel, ItemModelType
from .types.items import Item
from .types.entity import Entity
from .types.recipe import CookingRecipe, SmeltingRecipe, SmokingRecipe, CampfireRecipe, CraftingGrid, CraftingRecipe
from .config import config
from .logging import debug, info


class DataPack:
    def __init__(
            self,
            name: str = 'My DataPack',
            description: str = 'My awesome datapack',
            pack_format: PackFormat | int = PackFormat.latest(),
            assets_dir: str | None = './assets',
    ):
        self.name: str = name.replace(' ', '_').lower()
        self.description: str = description
        self.namespaces: list[Namespace] = []
        self.assets_dir: str | None = assets_dir

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

    @property
    def resource_mcmeta(self) -> dict[str, Any]:
        return {
            "pack": {
                "pack_format": 64,
                "description": f"Resources for {self.name}"
            }
        }
    
    def register(self, namespace: Namespace):
        self.namespaces.append(namespace)
    
    def unregister(self, namespace: Namespace):
        self.namespaces.remove(namespace)
    
    def _write(self, filename: str, data: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)

    def _export_resource_pack(self, zip_path: str):
        buf = io.BytesIO()

        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zipf:
            pack_meta = {
                "pack": {
                    "pack_format": self.pack_format,
                    "description": f"Resources for {self.name}"
                }
            }
            zipf.writestr("pack.mcmeta", dumps(pack_meta, indent=2))

            if self.assets_dir and os.path.exists(self.assets_dir):
                for root, _, files in os.walk(self.assets_dir):
                    rel_path = os.path.relpath(root, self.assets_dir)
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_name = os.path.join("assets", rel_path, file) if rel_path != "." else os.path.join("assets", file)
                        with open(file_path, "rb") as f:
                            zipf.writestr(zip_name.replace("\\", "/"), f.read())
            else:
                info("no assets found, skipping resource pack assets")

        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        with open(zip_path, "wb") as f:
            f.write(buf.getvalue())

        info(f'resource pack written to {zip_path}')

    def export(
            self,
            path: str | None = None,
            clean: bool = False
    ):
        if path is None:
            path = f'./exported/{self.name}'

        datapack_path = os.path.join(path, 'data')

        if os.path.exists(datapack_path) and clean:
            info('clean old datapack version ...')
            shutil.rmtree(datapack_path)

        info(f'export datapack to {path}')
        os.makedirs(datapack_path, exist_ok=True)

        info('export all namespaces ...')
        for namespace in self.namespaces:
            namespace.export(path)

        info('export datapack pack.mcmeta')
        self._write(f'{path}/pack.mcmeta', dumps(self.mcmeta, indent=2))

        abs_path = os.path.abspath(path)
        resource_pack_name = f'{self.name}'
        resource_pack_zip = f'{resource_pack_name}.zip'

        if '/saves/' in abs_path.replace('\\', '/'):
            # datapack внутри мира
            parts = abs_path.replace('\\', '/').split('/')
            try:
                saves_index = parts.index('saves')
                base_path = os.path.join('/', *parts[:saves_index])
                resourcepacks_path = os.path.join(base_path, 'resourcepacks', resource_pack_zip)
            except ValueError:
                resourcepacks_path = os.path.join(os.path.dirname(abs_path), resource_pack_zip)
        else:
            resourcepacks_path = os.path.join(os.path.dirname(abs_path), resource_pack_zip)

        info(f'creating resource pack archive → {resourcepacks_path}')
        self._export_resource_pack(resourcepacks_path)

        info('datapack exported successfully')
