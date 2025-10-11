import sys
from pathlib import Path
import argparse

from ..config import config
from .commands.create import create_project
from .commands.up import up_project
from .commands.dev import dev
from .commands.build import build_datapack


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(prog="chanty", description="Chanty CLI")
    subparsers = parser.add_subparsers(dest="command")

    # --- create ---
    create_parser = subparsers.add_parser("create", help="Create a new Chanty project")
    create_parser.add_argument("name", type=str, help="Project name")
    create_parser.add_argument("--debug", action="store_true", help="Enables debug mode and rich logging")
    create_parser.add_argument("--verbose", action="store_true", help="Verbose output")
    create_parser.set_defaults(func=lambda args: create_project(args.name))

    # --- up ---
    up_parser = subparsers.add_parser("up", help="Update your project to make it available on newer Chanty versions")
    up_parser.add_argument("--debug", action="store_true", help="Enables debug mode and rich logging")
    up_parser.add_argument("--verbose", action="store_true", help="Verbose output")
    up_parser.set_defaults(func=lambda _: up_project())

    # --- build ---
    build_parser = subparsers.add_parser("build", help="Build a datapack")
    build_parser.add_argument("target", type=str, help="Target pack, e.g., main:pack")
    build_parser.add_argument("--output", type=Path, help="Export folder")
    build_parser.add_argument("--to", type=Path, help="Export inside ./exported/project_name")
    build_parser.add_argument("--save_folder", type=Path, help="%APPDATA%/Roaming/.minecraft/saves/your_world/datapacks")
    build_parser.add_argument("--world_name", type=Path, help="your_world")
    build_parser.add_argument("--modrinth", type=Path, help="your_profile:your_world")
    build_parser.add_argument("--debug", action="store_true", help="Enables debug mode and rich logging")
    build_parser.add_argument("--verbose", action="store_true", help="Verbose output")
    build_parser.set_defaults(func=lambda args: build_datapack(
        args.target, args.output, args.to, args.save_folder, args.world_name, args.modrinth
    ))

    # --- dev ---
    dev_parser = subparsers.add_parser("dev", help="Start datapack development mode")
    dev_parser.add_argument("target", type=str, help="Target pack, e.g., main:pack")
    dev_parser.add_argument("--save_folder", type=Path, help="%APPDATA%/Roaming/.minecraft/saves/your_world/datapacks")
    dev_parser.add_argument("--world_name", type=Path, help="your_world")
    dev_parser.add_argument("--modrinth", type=Path, help="your_profile:your_world")
    dev_parser.add_argument("--debug", action="store_true", help="Enables debug mode and rich logging")
    dev_parser.add_argument("--verbose", action="store_true", help="Verbose output")
    dev_parser.set_defaults(func=lambda args: dev(args.target, args.save_folder, args.world_name, args.modrinth))


    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
