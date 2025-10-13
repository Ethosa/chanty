import sys
from pathlib import Path

import toml

from .logging import info
from ..types.namespace import Namespace
from ..command.builder import CommandBuilder
from ..command.condition import Unless
from ..types.custom_item import CustomItem, Item
from ..types.translations import Translations
from .. import DataPack


def get_project_name() -> str:
    """Try to get project name from pyproject.toml or current folder"""
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        try:
            data = toml.load(pyproject)
            return data.get("prject", {}).get("name", Path.cwd().name)
        except Exception:
            return Path.cwd().name
    return Path.cwd().name


def get_world_folder(world_folder_name: str, modrinth: bool = False) -> Path:
    """
    Return the full path to a Minecraft world folder by name.
    
    Args:
        world_folder_name (str): Name of the world folder.
    
    Returns:
        Path: Full path to the world folder.
    
    Raises:
        FileNotFoundError: If the world folder does not exist.
    """
    home = Path.home()

    if not modrinth:
        if sys.platform.startswith("win"):
            base = Path.home() / "AppData" / "Roaming" / ".minecraft" / "saves"
        elif sys.platform.startswith("darwin"):  # macOS
            base = home / "Library" / "Application Support" / "minecraft" / "saves"
        else:  # Linux / others
            base = home / ".minecraft" / "saves"
    else:
        profile, world_folder_name = str(world_folder_name).split(':')
        if sys.platform.startswith("win"):
            base = Path.home() / "AppData" / "Roaming" / "ModrinthApp" / "profiles" / profile / "saves"
        elif sys.platform.startswith("darwin"):  # macOS
            base = home / "Library" / "Application Support" / "ModrinthApp" / "profiles" / profile / "saves"
        else:  # Linux / others
            base = home / "ModrinthApp" / "profiles" / profile / "saves"

    world_path = base / world_folder_name

    if not world_path.exists() or not world_path.is_dir():
        raise FileNotFoundError(f"World folder '{world_folder_name}' not found in {base}")

    return world_path


def export_module(
        module_name: str,
        pack_name: str,
        save_folder: str,
        file_path: str | None = None,
        dev: bool = False
) -> DataPack:
    if module_name in sys.modules:
        del sys.modules[module_name]
    info(f"Building datapack ...")
    module = __import__(module_name)
    pack = getattr(module, pack_name)
    module.CustomItem._CUSTOM_ITEM_INDEX = 0

    if dev:
        dev_env = Namespace('dev_environment')
        pack.register(dev_env)

        chanty_debug = CustomItem(Item.STICK, custom_item_index='chanty_debug_stick')
        Translations.add('item.{project}.chanty_debugger', {
            'en_us': '§6§l[Chanty]§f§r Debugger',
            'ru_ru': '§6§l[Chanty]§f§r Отладчик',
        })
        Translations.add('item.{project}.chanty_debugger_lore_line1', {
            'en_us': 'Usage:',
            'ru_ru': 'Использование:',
        })
        Translations.add('item.{project}.chanty_debugger_lore_line2', {
            'en_us': '  §a§l[Right Click]§r: reload datapacks',
            'ru_ru': '  §a§l[ПКМ]§r: Перезагрузить датапаки',
        })
        chanty_debug.set_name('§6§l[Chanty]§f§r Debugger')
        chanty_debug.set_lore(
            'Usage:',
            '  §a§l[Right Click]§r: reload datapacks',
        )
        chanty_debug.glint(True)
        @chanty_debug.on_right_click
        def reload_datapacks():
            with CommandBuilder() as cmd:
                cmd._add('reload')
            return cmd.build()
        dev_env.register(chanty_debug)
        
        @dev_env.on_load
        def handle_on_load():
            with CommandBuilder() as cmd:
                if file_path:
                    cmd.tellraw([
                        {"text": "[Chanty] ", "color": "aqua", "bold": True},
                        {"text": "datapacks reloaded from ", "color": "gray"},
                        {"text": file_path, "color": "gold", "underlined": True},
                    ])
                else:
                    cmd.tellraw([
                        {"text": "[Chanty] ", "color": "aqua", "bold": True},
                        {"text": "datapacks reloaded", "color": "gray"}
                    ])
                with cmd.context(as_='@p') as me:
                    with cmd.context(condition=Unless(me.inventory.has_in_hotbar(chanty_debug)) & Unless(me.inventory.has_in_inventory(chanty_debug))):
                        cmd.give('@p', chanty_debug)
            return cmd.build()
    
    datapack_folder = f'{save_folder}/datapacks/{pack.name}'
    info(f"Exporting to [cyan]{datapack_folder}[/cyan]")
    pack.export(datapack_folder, clean=not dev)
