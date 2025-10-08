from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chanty.command.builder import CommandBuilder


class ScoreboardContext:
    def __init__(self, parent: CommandBuilder):
        self._p = parent
    
    def add(self, name: str, criteria: str = 'dummy') -> CommandBuilder:
        self._p._add(f'scoreboard objectvies add {name} {criteria}')
        return self._p
    
    def remove(self, name: str) -> CommandBuilder:
        self._p._add(f'scoreboard objectvies remove {name}')
        return self._p
    
    def list(self) -> CommandBuilder:
        self._p._add('scoreboard objectives list')
        return self._p
    
    def set(self, target: str, name: str, value: int) -> CommandBuilder:
        self._p._add(f'scoreboard players set {target} {name} {value}')
        return self._p
    
    def add_score(self, target: str, name: str, value: int) -> CommandBuilder:
        self._p._add(f'scoreboard players add {target} {name} {value}')
        return self._p
    
    def get(self, target: str, name: str) -> CommandBuilder:
        self._p._add(f'scoreboard players get {target} {name}')
        return self._p
    
    def reset(self, target: str, name: str | None = None) -> CommandBuilder:
        if name:
            self._p._add(f'scoreboard players reset {target} {name}')
        else:
            self._p._add(f'scoreboard players reset {target}')
        return self._p
