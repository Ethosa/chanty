from __future__ import annotations
from datetime import timedelta
from contextlib import contextmanager
from json import dumps
from typing import Any, Literal, Sequence, TYPE_CHECKING, overload

from .scoreboard_context import ScoreboardContext
from .selector_context import SelectorContext
from .condition import Condition, extract_or_groups
from .random import Random
from ..types.position import Coord
if TYPE_CHECKING:
    from .types import AnyItem, AnyPos, AnyFunction


class CommandBuilder:
    def __init__(self):
        self.commands: list[str] = []
        self._prefixes: list[str] = []
        self.scoreboard = ScoreboardContext(self)
        self.me = SelectorContext(self)

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

    def raw(self, line: str) -> CommandBuilder:
        """
        Executes raw command
        """
        self._add(line)
        return self

    def tellraw(
            self,
            message: str | Sequence[dict[str, Any]],
            target: str = "@a",
            **style
    ) -> CommandBuilder:
        if isinstance(message, str):
            component = {"text": message, **style}
            json_message = dumps(component, ensure_ascii=False)
        elif isinstance(message, (list, tuple)):
            json_message = dumps(message, ensure_ascii=False)
        else:
            raise TypeError("message must be str or list[dict]")

        self._add(f"tellraw {target} {json_message}")
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
            if isinstance(pos, Random):
                with pos.build(self):
                    self._add(f"execute as {pos.target} at @s run setblock ~ ~ ~ {block}")
            else:
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
            if isinstance(pos, Random):
                with pos.build(self):
                    self._add(f"execute as {pos.target} at @s run tp ~ ~ ~ facing entity {facing_entity} {facing}")
            else:
                self._add(f'tp {target} {" ".join(pos)} facing entity {facing_entity} {facing}')
        else:
            if isinstance(pos, Random):
                with pos.build(self):
                    self._add(f"execute as {pos.target} at @s run tp ~ ~ ~")
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
        if isinstance(pos, Random):
            with pos.build(self):
                self._add(f"execute as {pos.target} at @s run summon {entity} ~ ~ ~")
        else:
            self._add(f"summon {entity} {' '.join(pos)}")
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
        if_: str | list[str] | None = None,
        unless: str | list[str] | None = None,
        facing_entity: str | None = None,
        facing: Literal["eyes", "feet"] | None = 'eyes',
        condition: Condition | None = None,
    ):
        parts = ["execute"]

        if as_:
            parts.append(f"as {as_}")
        if at:
            parts.append(f"at {at}")

        or_groups = []
        tmp_prefixes = []

        if condition is not None:
            or_groups = extract_or_groups(condition)
            for group in or_groups:
                tmp_name = f"__chanty_tmp_or_{group.group_id}"
                self._add(f"scoreboard objectives add {tmp_name} dummy")
                self._add(f"scoreboard players set var {tmp_name} 0")

                for sub in group.or_groups:
                    for prefix, cond in sub.conditions:
                        self._add(f"execute {prefix} {cond} run scoreboard players add var {tmp_name} 1")

            execute_prefix = []
            for group in or_groups:
                execute_prefix.append(f"if score var __chanty_tmp_or_{group.group_id} matches 1..")
            for prefix, cond in condition.conditions:
                execute_prefix.append(f"{prefix} {cond}")
            tmp_prefixes.append(" ".join(execute_prefix))

        if if_:
            if isinstance(if_, str):
                tmp_prefixes.append(f"if {if_}")
            else:
                tmp_prefixes.append(" ".join([f"if {c}" for c in if_]))
        if unless:
            if isinstance(unless, str):
                tmp_prefixes.append(f"unless {unless}")
            else:
                tmp_prefixes.append(" ".join([f"unless {c}" for c in unless]))
        if facing_entity:
            tmp_prefixes.append(f"facing entity {facing_entity} {facing}")

        if tmp_prefixes:
            parts.append(" ".join(tmp_prefixes))
        parts.append("run")

        prefix = " ".join(parts)
        self._prefixes.append(prefix)

        try:
            if as_:
                yield SelectorContext(as_)
            else:
                yield None
        finally:
            self._prefixes.pop()
            for group in or_groups:
                tmp_name = f"__chanty_tmp_or_{group.group_id}"
                self._add(f"scoreboard objectives remove {tmp_name}")
    
    def build(self) -> str:
        return '\n'.join(self.commands)
