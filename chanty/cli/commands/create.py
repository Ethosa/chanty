import os
import sys
from pathlib import Path

from rich.panel import Panel

from ..logging import info, error, success, console


PROJECT_TEMPLATE = {
    "main.py": '''from chanty import DataPack, Namespace, CommandBuilder

pack = DataPack('{name}')
namespace = Namespace('main')
pack.register(namespace)


@namespace.on_load
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
    "pyproject.toml": '''[project]
name = "{name}"
version = "0.1.0"
description = "Minecraft Datapack made with Chanty"
authors = [
    {{ name = "Your Name", email = "you@example.com" }}
]
requires-python = ">=3.11"
dependencies = [
    "chanty>=0.1.1",
]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["{name}"]
'''
}


def create_project(name: str):
    project_path = Path(name)
    assets_textures_folder = Path(name) / 'assets' / name / 'textures' / 'item'
    assets_models_folder = Path(name) / 'assets' / name / 'models' / 'item'
    assets_atlases_folder = Path(name) / 'assets' / name / 'items'

    if project_path.exists():
        error(f"Directory [yellow]'{name}'[/yellow] already exists")
        sys.exit(1)

    info(f"Creating project '{name}'...")

    project_path.mkdir(parents=True)
    assets_textures_folder.mkdir(parents=True)
    assets_models_folder.mkdir(parents=True)
    assets_atlases_folder.mkdir(parents=True)
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
