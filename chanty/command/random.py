from __future__ import annotations
from random import randint
from typing import TYPE_CHECKING
from contextlib import contextmanager

from ..types.position import Position
if TYPE_CHECKING:
    from .builder import CommandBuilder


class Random:
    def __init__(
            self,
            center: Position | None = None,
            spread_min: int = 2,
            spread_max: int = 10
    ):
        if center is None:
            center = Position.CURRENT
        self.center = center
        self.spread_min = spread_min
        self.spread_max = spread_max

        self._commands_pre = []
        self._commands_after = []

        self._generate_internal()

    def _generate_internal(self):
        tag = f"rand_{randint(0, 1_000_000)}"
        self.target = f"@e[type=armor_stand,tag={tag},limit=1]"
        cx, cy, cz = self.center._x, self.center._y, self.center._z

        self._commands_pre.append(
            f"summon minecraft:armor_stand {cx} {cy} {cz} {{Tags:[\"{tag}\"],NoGravity:1b,Invisible:1b}}"
        )
        self._commands_pre.append(
            f"spreadplayers {cx} {cz} {self.spread_min} {self.spread_max} false {self.target}"
        )
        self._commands_after.append(f"kill {self.target}")

    def __iter__(self):
        return iter(["~", "~", "~"])
    
    @contextmanager
    def build(self, builder: CommandBuilder):
        for cmd in self._commands_pre:
            builder._add(cmd)
        yield
        for cmd in self._commands_after:
            builder._add(cmd)
