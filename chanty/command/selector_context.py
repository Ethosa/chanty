from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import AnyItem


class SelectorContext:
    def __init__(self, selector: str):
        self.selector = selector
        self.inventory = _InventoryContext(selector)


class _InventoryContext:
    def __init__(self, selector: str):
        self.selector = selector

    def has(self, item: AnyItem) -> str:
        return f'items entity {self.selector} inventory.* {str(item)}'

    def has_in_inventory(self, item: AnyItem) -> str:
        return f'items entity {self.selector} inventory.* {str(item)}'

    def has_in_hotbar(self, item: AnyItem) -> str:
        return f'items entity {self.selector} hotbar.* {str(item)}'

    def has_in_enderchest(self, item: AnyItem) -> str:
        return f'items entity {self.selector} enderchest.* {str(item)}'

    def in_horse(self, item: AnyItem) -> str:
        return f'items entity {self.selector} horse.* {str(item)}'

    def has_weapon(self, item: AnyItem) -> str:
        return f'items entity {self.selector} weapon.* {str(item)}'

    def has_armor(self, item: AnyItem) -> str:
        return f'items entity {self.selector} armor.* {str(item)}'

    def has_in_container(self, item: AnyItem) -> str:
        return f'items entity {self.selector} container.* {str(item)}'

    def has_in_slot(self, slot: str, item: AnyItem) -> str:
        return f'items entity {self.selector} {slot} {str(item)}'
