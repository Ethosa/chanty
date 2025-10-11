from pathlib import Path

from rich.panel import Panel

from ..logging import success, console
from ..utils import export_module, get_project_name, get_world_folder

def build_datapack(
        target: str,
        output: Path | None = None,
        to: Path | None = None,
        save_folder: str | None = None,
        world_name: str | None = None,
        modrinth: str | None = None,
):
    """Import the pack and export to folder"""
    if save_folder is None and world_name is None and modrinth is None:
        if to:
            project_name = get_project_name()
            save_folder = Path(to) / project_name
        elif output:
            save_folder = Path(output)
        else:
            save_folder = Path("./exported") / get_project_name()
    if save_folder is None and world_name is not None:
        save_folder = get_world_folder(world_name)
    if save_folder is None and modrinth is not None:
        save_folder = get_world_folder(modrinth, modrinth=True)

    module_name, pack_name = target.split(":")
    export_module(module_name, pack_name, save_folder)
    success("Build complete!")
    console.print(Panel(f"Datapack exported to: {save_folder}", title="Chanty", style="green"))
