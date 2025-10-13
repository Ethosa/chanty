import sys
from pathlib import Path

from rich.panel import Panel

from ..logging import info, error, success, console
from .create import PROJECT_TEMPLATE


def up_project():
    current_folder = Path.cwd()
    project_name = current_folder.name

    info(f"Checking project '{project_name}' structure...")

    assets_paths = [
        current_folder / 'assets' / current_folder.parts[-1] / 'textures' / 'item',
        current_folder / 'assets' / current_folder.parts[-1] / 'models' / 'item',
        current_folder / 'assets' / current_folder.parts[-1] / 'items',
    ]
    
    created_dirs = 0
    for folder in assets_paths:
        if not folder.exists():
            folder.mkdir(parents=True)
            info(f"Created missing folder: [green]{folder}[/green]")
            created_dirs += 1
    
    created_files = 0
    for filename, content in PROJECT_TEMPLATE.items():
        file_path = current_folder / filename
        if '/' in filename:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            content = content.format(name=project_name, project_name=project_name)
            file_path.write_text(content, encoding="utf-8")
            info(f"Added missing file: [green]{filename}[/green]")
            created_files += 1
    
    if created_dirs == 0 and created_files == 0:
        success("Your project structure is already up to date!")
    else:
        success(f"Project '{project_name}' updated successfully.")
        console.print(Panel(
            f"[b]Added {created_files} file(s)[/b]\n"
            f"[b]Created {created_dirs} folder(s)[/b]\n"
            f"Path: {current_folder}",
            title="Chanty Up",
            style="cyan"
        ))
