from abc import abstractmethod, ABC
from datetime import timedelta
from enum import Enum
from typing import Any

from .items import Item


class Recipe(ABC):
    id: str

    @abstractmethod
    def to_json(self) -> dict[str, Any]:
        ...


class CookingRecipe(Recipe):
    recipe_type: str = ''

    def __init__(
            self,
            id: str,
            ingredient: str | Item,
            result: str | Item,
            experience: float = 0.1,
            cooking_time: int | timedelta | None = None,
            group: str | None = None,
            recipe_type: str | None = None,
    ):
        self.id = id
        self.ingredient = str(ingredient)
        self.result = str(result)
        self.experience = experience
        if isinstance(cooking_time, timedelta):
            cooking_time = int(cooking_time.total_seconds() * 20)
        self.cooking_time = cooking_time
        self.group = group
        if recipe_type is not None:
            self.recipe_type = recipe_type

    def to_json(self) -> dict[str, Any]:
        data = {
            'type': self.recipe_type,
            'ingredient': self.ingredient,
            'result': {
                'id': self.result
            },
            'experience': float(self.experience)
        }
        if self.cooking_time is not None:
            data['cookingtime'] = self.cooking_time
        if self.group is not None:
            data['group'] = self.group
        return data


class BlastingRecipe(CookingRecipe):
    recipe_type: str = 'minecraft:blasting'


class CampfireRecipe(CookingRecipe):
    recipe_type: str = 'minecraft:campfire_cooking'


class SmeltingRecipe(CookingRecipe):
    recipe_type: str = 'minecraft:smelting'


class SmokingRecipe(CookingRecipe):
    recipe_type: str = 'minecraft:smoking'


class CraftingGrid(int, Enum):
    FIELD_2X2 = 2
    FIELD_3X3 = 3


class CraftingRecipe(Recipe):
    def __init__(
            self,
            id: str,
            ingredients: list[str | Item] | list[list[str | Item]],
            result: str | Item,
            result_count: int = 1,
            size: int | CraftingGrid = CraftingGrid.FIELD_3X3,
            shapeless: bool = False,
            strict: bool = False,
    ):
        self.id = id
        if isinstance(size, CraftingGrid):
            self.size = size.value
        elif isinstance(size, int):
            self.size = size
        else:
            raise TypeError("size must be int or CraftingGrid")

        if self.size not in (2, 3):
            raise ValueError("crafting recipe size must be 2 or 3")
        self.shapeless = shapeless
        self.strict = strict
        self.result = str(result)
        self.result_count = result_count
        self.ingredients = ingredients

    def to_json(self) -> dict[str, Any]:
        data = {
            'result': {
                'id': self.result,
                'count': self.result_count
            }
        }
        if self.shapeless:
            data['ingredients'] = self.ingredients
            data['type'] = 'minecraft:crafting_shapeless'
            return data
        data["type"] = "minecraft:crafting_shaped"
        grid = self.ingredients
        if not self.strict:
            def empty_row(row): return all(x in (None, "", " ") for x in row)
            while grid and empty_row(grid[0]): grid.pop(0)
            while grid and empty_row(grid[-1]): grid.pop(-1)
            if grid:
                left = 0
                right = self.size - 1
                while all(r[left] in (None, "", " ") for r in grid) and left < self.size:
                    left += 1
                while all(r[right] in (None, "", " ") for r in grid) and right >= 0:
                    right -= 1
                grid = [r[left:right + 1] for r in grid]
        pattern = []
        key = {}
        symbol_iter = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        symbol_map: dict[str, str] = {}

        for row in grid:
            line = ""
            for cell in row:
                if cell in (None, "", " "):
                    line += " "
                    continue
                if cell not in symbol_map:
                    symbol = next(symbol_iter)
                    symbol_map[cell] = symbol
                    key[symbol] = str(cell)
                line += symbol_map[str(cell)]
            pattern.append(line)

        data["pattern"] = pattern
        data["key"] = key
        return data
