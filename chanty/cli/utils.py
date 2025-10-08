import sys
from pathlib import Path

import toml


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
