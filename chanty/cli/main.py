import sys
from pathlib import Path
import argparse

from rich.panel import Panel
from watchfiles import watch

from ..types.namespace import Namespace
from ..command.builder import CommandBuilder
from ..command.condition import Unless
from ..custom_item import CustomItem, Item
from .. import DataPack
from .utils import get_project_name, get_world_folder
from .logging import console, success, info, error


PROJECT_TEMPLATE = {
    "main.py": '''from chanty import DataPack, Namespace, CommandBuilder

pack = DataPack('{name}')
namespace = Namespace('main')
pack.register_namespace(namespace)


@namespace.onload
def handle_on_load() -> str:
    with CommandBuilder() as cmd:
        cmd.tellraw("Hello from your Chanty project <3")
    return cmd.build()


if __name__ == "__main__":
    pack.export('./exported/{name}')
''',
    "requirements.txt": "chanty>=0.1.1\n",
    "README.md": "# {name}\n### Made with Chanty <3\n",
    ".gitignore": "__pycache__/\ndist/\n.vscode/\n.pytest_cache/\nexported/\n",
}


def create_project(name: str):
    project_path = Path(name)
    if project_path.exists():
        error(f"Directory [yellow]'{name}'[/yellow] already exists")
        sys.exit(1)

    info(f"Creating project '{name}'...")

    project_path.mkdir(parents=True)
    for filename, content in PROJECT_TEMPLATE.items():
        file_path = project_path / filename
        content = content.format(name=name, project_name=name)
        file_path.write_text(content, encoding="utf-8")
        info(f"Created [green]{filename}[/green]")

    success(f"Project [yellow]'{name}'[/yellow] created successfully!")
    console.print(Panel(
        f"[b]Next steps[/b]\n"
        f"  cd {name}\n"
        f"  pip install -r requirements.txt\n"
        f"  python main.py",
        title="Chanty",
        style="cyan"
    ))


def _export_module(
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

    if dev:
        dev_env = Namespace('dev_environment')
        pack.register_namespace(dev_env)

        chanty_debug = CustomItem(Item.STICK, custom_item_index='chanty_debug_stick')
        chanty_debug.set_name('§6§l[Chanty]§f§r Debugger')
        chanty_debug.set_lore(
            'This is a not just stick ...',
            'This is a §6§l[Chanty]§f§r Debugger!',
        )
        chanty_debug.glint(True)
        @chanty_debug.on_right_click
        def reload_datapacks():
            with CommandBuilder() as cmd:
                cmd._add('reload')
            return cmd.build()
        dev_env.register(chanty_debug)
        
        @dev_env.onload
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
    pack.export(datapack_folder)


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

    _export_module(module_name, pack_name, save_folder, dev=True)

    info(f"Loaded pack from {module_name}")

    src_path = Path.cwd()

    for changes in watch(src_path):
        for change_type, filepath in changes:
            file_path = filepath
            if not file_path.endswith(".py"):
                continue
            info(f"Detected change in {file_path}")
            try:
                _export_module(module_name, pack_name, save_folder, file_path, dev=True)
                success("Module reloaded successfully")
                info("Please use [yellow]/reload[/yellow] command or Chanty Debugger in your game.")
                break
            except Exception as e:
                error(f"Error reloading {file_path}: {e}")


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
    _export_module(module_name, pack_name, save_folder)
    success("Build complete!")
    console.print(Panel(f"Datapack exported to: {save_folder}", title="Chanty", style="green"))


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(prog="chanty", description="Chanty CLI")
    subparsers = parser.add_subparsers(dest="command")

    # --- create ---
    create_parser = subparsers.add_parser("create", help="Create a new Chanty project")
    create_parser.add_argument("name", type=str, help="Project name")
    create_parser.set_defaults(func=lambda args: create_project(args.name))

    # --- build ---
    build_parser = subparsers.add_parser("build", help="Build a datapack")
    build_parser.add_argument("target", type=str, help="Target pack, e.g., main:pack")
    build_parser.add_argument("--output", type=Path, help="Export folder")
    build_parser.add_argument("--to", type=Path, help="Export inside ./exported/project_name")
    build_parser.add_argument("--save_folder", type=Path, help="%APPDATA%/Roaming/.minecraft/saves/your_world/datapacks")
    build_parser.add_argument("--world_name", type=Path, help="your_world")
    build_parser.add_argument("--modrinth", type=Path, help="your_profile:your_world")
    build_parser.set_defaults(func=lambda args: build_datapack(
        args.target, args.output, args.to, args.save_folder, args.world_name, args.modrinth
    ))

    # --- dev ---
    build_parser = subparsers.add_parser("dev", help="Start datapack development mode")
    build_parser.add_argument("target", type=str, help="Target pack, e.g., main:pack")
    build_parser.add_argument("--save_folder", type=Path, help="%APPDATA%/Roaming/.minecraft/saves/your_world/datapacks")
    build_parser.add_argument("--world_name", type=Path, help="your_world")
    build_parser.add_argument("--modrinth", type=Path, help="your_profile:your_world")
    build_parser.set_defaults(func=lambda args: dev(args.target, args.save_folder, args.world_name, args.modrinth))


    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
