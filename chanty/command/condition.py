from __future__ import annotations
from itertools import count


class Condition:
    _id_counter = count(1)

    def __init__(self, condition: str | None = None, prefix: str = '', is_or_group=False):
        self.conditions: list[tuple[str, str]] = []
        if condition:
            self.conditions.append((prefix, condition))
        self.is_or_group = is_or_group
        self.or_groups: list[Condition] = []
        self.group_id = None

    def __and__(self, other: 'Condition') -> 'Condition':
        new = Condition()
        new.conditions = self.conditions + other.conditions
        new.or_groups = self.or_groups + other.or_groups
        return new

    def __or__(self, other: 'Condition') -> 'Condition':
        new = Condition(is_or_group=True)
        new.or_groups = [self, other]
        new.group_id = next(self._id_counter)
        return new


class If(Condition):
    def __init__(self, cond: str):
        super().__init__(cond, 'if')


class Unless(Condition):
    def __init__(self, cond: str):
        super().__init__(cond, 'unless')


def extract_or_groups(condition: Condition) -> list[Condition]:
    groups = []
    if condition.is_or_group:
        groups.append(condition)
    for sub in getattr(condition, "or_groups", []):
        groups += extract_or_groups(sub)
    return groups
