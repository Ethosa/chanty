import os
from json import dumps
from enum import Enum

from ..utils import detect_project_name


class ItemModelType(str, Enum):
    HANDHELD = 'handheld'
    GENERATED = 'generated'
    
    def __str__(self) -> str:
        return self.value


class CustomModel:
    def __init__(
            self,
            name: str,
            parent: str | ItemModelType = ItemModelType.GENERATED
    ):
        self.name = name
        self.parent = str(parent)
        self.project_name = detect_project_name()
        self.base_assets_path = os.path.join("assets", self.project_name)

        # пути
        self.items_dir = os.path.join(self.base_assets_path, "items")
        self.models_dir = os.path.join(self.base_assets_path, "models", "item")

        os.makedirs(self.items_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)

        self.texture = f"{self.project_name}:item/{self.name}"

        self._create_files()

    def _create_files(self):
        items_json = {
            "model": {
                "type": "minecraft:model",
                "model": f"{self.project_name}:item/{self.name}"
            }
        }
        with open(os.path.join(self.items_dir, f"{self.name}.json"), "w", encoding="utf-8") as f:
            f.write(dumps(items_json, indent=2))

        models_json = {
            "parent": f"item/{self.parent}",
            "textures": {
                "layer0": self.texture
            }
        }
        with open(os.path.join(self.models_dir, f"{self.name}.json"), "w", encoding="utf-8") as f:
            f.write(dumps(models_json, indent=2))

    def __str__(self):
        return f"{self.project_name}:{self.name}"
