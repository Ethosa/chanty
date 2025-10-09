import sys
import argparse
from typing import Any


class ChantyConfig:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(
            prog="chanty",
            description="Chanty CLI and runtime configuration"
        )
        self._register_arguments()
        self._args, self._extra = self._parser.parse_known_args(sys.argv[1:])

    def _register_arguments(self):
        self._parser.add_argument("--debug", action="store_true", help="Enables debug mode and rich logging")
        self._parser.add_argument("--verbose", action="store_true", help="Verbose output")

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self._args, key, default)

    def has_flag(self, flag: str) -> bool:
        val = getattr(self._args, flag, None)
        return bool(val)

    def __getattr__(self, item: str) -> Any:
        return self.get(item)

    def __repr__(self) -> str:
        args = vars(self._args)
        return f"<ChantyConfig {args}>"

    def __contains__(self, item: str) -> bool:
        return item in vars(self._args)


config = ChantyConfig()
