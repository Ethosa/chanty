import sys
from pathlib import Path

from watchfiles import watch

from ..logging import info, error, success
from ..utils import get_project_name, export_module, get_world_folder


def dev(
        target: str,
        save_folder: str | None = None,
        world_name: str | None = None,
        modrinth: str | None = None,
):
    module_name, pack_name = target.split(":")
    sys.path.insert(0, str(Path.cwd()))
    if save_folder is None and world_name is None and modrinth is None:
        error(f"You should pass the --save_folder, --modrinth or --world_name param!")
        return
    if save_folder is None and world_name is not None:
        save_folder = get_world_folder(world_name)
    if save_folder is None and modrinth is not None:
        save_folder = get_world_folder(modrinth, modrinth=True)

    export_module(module_name, pack_name, save_folder, dev=True)

    info(f"Loaded pack from {module_name}")

    src_path = Path.cwd()

    for changes in watch(src_path):
        for change_type, filepath in changes:
            file_path = filepath
            if not file_path.endswith(".py"):
                continue
            info(f"Detected change in {file_path}")
            try:
                export_module(module_name, pack_name, save_folder, file_path, dev=True)
                success("Module reloaded successfully")
                info("Please use [yellow]/reload[/yellow] command or Chanty Debugger in your game.")
                break
            except Exception as e:
                error(f"Error reloading {file_path}: {e}")
