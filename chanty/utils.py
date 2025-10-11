import os

import toml


def detect_project_name() -> str:
    if os.path.exists("pyproject.toml"):
        try:
            data = toml.load("pyproject.toml")
            name = (
                data.get("project", {}).get("name")
                or data.get("tool", {}).get("poetry", {}).get("name")
            )
            if name:
                return name.lower()
        except Exception:
            pass
    return os.path.basename(os.getcwd()).lower()
