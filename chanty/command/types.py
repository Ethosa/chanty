from __future__ import annotations
from typing import Iterable, Union, Callable, TYPE_CHECKING

from ..types.items import Item
from ..types.position import Position
from ..custom_item import CustomItem
import chanty.command.builder as builder


AnyPos = Union[Iterable[str | int], Position]
AnyItem = Union[str, Item, CustomItem]
AnyFunction = Union[str, Callable[[], Union[str, builder.CommandBuilder]]]
