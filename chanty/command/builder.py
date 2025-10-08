from __future__ import annotations
from datetime import timedelta
from contextlib import contextmanager
from typing import Literal, TYPE_CHECKING, overload

from .scoreboard_context import ScoreboardContext
from ..types.position import Coord
if TYPE_CHECKING:
    from .types import AnyItem, AnyPos, AnyFunction


class CommandBuilder:
    def __init__(self):
        self.commands: list[str] = []
        self._prefixes: list[str] = []
        self.scoreboard = ScoreboardContext(self)

    def __enter__(self) -> CommandBuilder:
        return self

    def __exit__(
            self,
            exc_type: type | None,
            exc_val: BaseException | None,
            exc_tb: type | None
    ):
        pass

    def _add(self, line: str):
        if self._prefixes:
            full_prefix = " ".join(self._prefixes)
            self.commands.append(f"{full_prefix} {line}")
        else:
            self.commands.append(line)

    def tellraw(self, message: str, target: str = "@a") -> CommandBuilder:
        self._add(f'tellraw {target} {{"text":"{message}"}}')
        return self

    def say(self, message: str) -> CommandBuilder:
        self._add(f'say {message}')
        return self

    @overload
    def set_block(self, block: AnyItem, pos: AnyPos) -> CommandBuilder: ...

    @overload
    def set_block(self, block: AnyItem, x: Coord, y: Coord, z: Coord) -> CommandBuilder: ...

    def set_block(self, block: AnyItem, *args) -> CommandBuilder:
        if len(args) == 1:
            pos = args[0]
            self._add(f'setblock {" ".join(pos)} {str(block)}')
        elif len(args) == 3:
            x, y, z = args
            self._add(f'setblock {x} {y} {z} {block}')
        else:
            raise TypeError("set_block expects 1 position or 3 coordinates")
        return self

    def fill(
            self,
            frm: AnyPos,
            to: AnyPos,
            block: AnyItem,
            mode: Literal['destroy', 'hollow', 'keep', 'outline', 'replace'] = 'replace'
    ) -> CommandBuilder:
        self._add(f'fill {" ".join(frm)} {" ".join(to)} {str(block)} {mode}')
        return self

    def give(self, target: str, item: AnyItem, count: int = 1) -> CommandBuilder:
        self._add(f'give {target} {str(item)} {count}')
        return self
    
    def effect(
            self,
            target: str,
            effect: str,
            duration: int = 60,
            amplifier: int = 1,
            hide_particles: bool = False
    ) -> CommandBuilder:
        if hide_particles:
            self._add(f'effect give {target} {effect} {duration} {amplifier} true')
        else:
            self._add(f'effect give {target} {effect} {duration} {amplifier}')
        return self
    
    def weather(
            self,
            weather_type: Literal['clear', 'rain', 'thunder'],
            duration: int | None = None
    ) -> CommandBuilder:
        if duration:
            self._add(f'weather {weather_type} {duration}')
        else:
            self._add(f'weather {weather_type}')
        return self
    
    def time(
            self,
            time: Literal['day', 'night', 'noon', 'midnight'] | int
    ) -> CommandBuilder:
        self._add(f'time set {time}')
        return self

    def tp(
            self,
            target: str,
            pos: AnyPos,
            facing_entity: str | None = None,
            facing: Literal['feet', 'eyes'] = 'eyes'
    ) -> CommandBuilder:
        if facing_entity:
            self._add(f'tp {target} {" ".join(pos)} facing entity {facing_entity} {facing}')
        else:
            self._add(f'tp {target} {" ".join(pos)}')
        return self

    def rotate(self, target: str, pos: AnyPos | str) -> CommandBuilder:
        if isinstance(pos, str):
            self._add(f'rotate {target} facing {pos}')
        else:
            self._add(f'rotate {target} facing {" ".join(pos)}')
        return self

    def summon(self, entity: str, pos: AnyPos) -> CommandBuilder:
        self._add(f'summon {entity} {" ".join(pos)}')
        return self

    def call(self, target: AnyFunction) -> CommandBuilder:
        if isinstance(target, str):
            self._add(f'function {target}')
        elif hasattr(target, 'id'):
            self._add(f'function {target.id}')
        return self

    def call_later(
            self,
            target: AnyFunction,
            time: timedelta | str,
            mode: Literal['append', 'replace'] = 'replace'
    ) -> CommandBuilder:
        if isinstance(time, timedelta):
            time = f'{time.total_seconds()}s'
        if isinstance(target, str):
            self._add(f'schedule function {target} {time} {mode}')
        elif hasattr(target, 'id'):
            self._add(f'schedule function {target.id} {time} {mode}')
        return self
    
    @contextmanager
    def context(
        self,
        as_: str | None = None,
        at: str | None = None,
        if_: str | None = None,
        unless: str | None = None,
        condition: str | None = None,
        facing_entity: str | None = None,
        facing: Literal["eyes", "feet"] | None = None
    ):
        parts = ["execute"]
        if as_: parts.append(f"as {as_}")
        if at: parts.append(f"at {at}")
        if if_: parts.append(f"if {if_}")
        if unless: parts.append(f"unless {unless}")
        if condition: parts.append(f"if {condition}")
        if facing_entity:
            parts.append(f"facing entity {facing_entity} {facing or 'eyes'}")
        parts.append('run')
        prefix = " ".join(parts)
        self._prefixes.append(prefix)
        try:
            yield self
        finally:
            self._prefixes.pop()
    
    def build(self) -> str:
        return '\n'.join(self.commands)
