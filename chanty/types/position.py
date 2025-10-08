from __future__ import annotations
from typing import Iterable, Iterator, Union, Optional
import math


Coord = Optional[Union[int, float, str]]


class Position(Iterable[str]):
    """
    Represents a 3D position in Minecraft coordinates, supporting
    absolute, relative (~), and direction (^) coordinates.  
    Supports arithmetic operations and conversion to string/tuple.

    Examples:
        >>> Position(1, 2, 3) + Position.VIEW
        >>> Position.CURRENT - Position(5, 4)
        >>> ((Position(1) * Position(5, 2, 8)) + Position.VIEW) * -1
    """
    __slots__ = ("_x", "_y", "_z")

    VIEW: 'Position'
    CURRENT: 'Position'

    VIEW = None
    CURRENT = None
    
    def __init__(
            self,
            x: Coord = None,
            y: Coord = None,
            z: Coord = None
    ):
        """
        Initialize a Position.

        Args:
            x (Coord): X coordinate (absolute, current position "~", or current direction "^").
            y (Coord): Y coordinate (optional, defaults to x if only x is provided).
            z (Coord): Z coordinate (optional, defaults to '~' if not specified).
        """
        if x is not None and y is None and z is None:
            y = z = x
        elif z is None:
            z = '~'
        elif y is None:
            y = '~'
        if x is None:
            x = '~'

        self._x = self._normalize(x)
        self._y = self._normalize(y)
        self._z = self._normalize(z)
    
    @property
    def x(self) -> float:
        if self._x.startswith(('~', '^')):
            raise ValueError("Cannot perform numeric operations on relative coordinates")
        return float(self._x)

    @x.setter
    def x(self, value: float):
        self._x = str(value)

    @property
    def y(self) -> float:
        if self._y.startswith(('~', '^')):
            raise ValueError("Cannot perform numeric operations on relative coordinates")
        return float(self._y)

    @y.setter
    def y(self, value: float):
        self._y = str(value)

    @property
    def z(self) -> float:
        if self._z.startswith(('~', '^')):
            raise ValueError("Cannot perform numeric operations on relative coordinates")
        return float(self._z)

    @z.setter
    def z(self, value: float):
        self._z = str(value)

    def _normalize(self, value: int | float | str) -> str:
        """
        Converts coord into string
        Allows "~1", "^2", "~", "^".
        """
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            value = value.strip()
            if value.startswith(("~", "^")):
                if len(value) == 1:
                    return value
                try:
                    float(value[1:])
                    return value
                except ValueError:
                    raise ValueError("Cannot perform numeric operations on relative coordinates")
            else:
                try:
                    float(value)
                    return value
                except ValueError:
                    raise ValueError(f"Invalid numeric coordinate: {value}")
        raise TypeError(f"Unsupported coordinate type: {type(value)}")

    def __iter__(self) -> Iterator[str]:
        """Iterate over X, Y, Z as strings."""
        yield self._x
        yield self._y
        yield self._z

    def __repr__(self) -> str:
        return f"Position({self._x}, {self._y}, {self._z})"

    def __str__(self) -> str:
        """Return coordinates as space-separated string."""
        return f"{self._x} {self._y} {self._z}"

    def copy(self) -> Position:
        """Return a copy of this Position."""
        return Position(self._x, self._y, self._z)

    def as_tuple(self) -> tuple[str, str, str]:
        """Return coordinates as a tuple of strings."""
        return (self._x, self._y, self._z)

    def _to_float(self, val: str) -> float:
        """Convert absolute coordinate string to float."""
        if val.startswith(("~", "^")):
            raise ValueError(f"Cannot perform arithmetic with relative coordinates: {val}")
        return float(val)

    
    @staticmethod
    def _to_position(value: Position | tuple | list | int | float) -> Position:
        """Convert input to Position object."""
        if isinstance(value, Position):
            return value
        if isinstance(value, (tuple, list)):
            if len(value) == 1:
                return Position(value[0])
            if len(value) == 3:
                return Position(*value)
            raise ValueError("Tuple/list must have 1 or 3 elements")
        if isinstance(value, (int, float)):
            return Position(value)
        raise TypeError(f"Cannot convert {type(value)} to Position")

    def _combine(self, left: str, right: str, op: str) -> str:
        for prefix in ('~', '^'):
            if left == prefix and not right.startswith(('~', '^')):
                sign = '' if op == '+' else '-'
                return f"{prefix}{sign}{right}"
            if right == prefix and not left.startswith(('~', '^')):
                sign = '' if op == '+' else '-'
                return f"{prefix}{sign}{left}"
            if left.startswith(prefix) and right.startswith(prefix):
                if left[1:] == '' or right[1:] == '':
                    return prefix
                l, r = float(left[1:]), float(right[1:])
                val = l + r if op == '+' else l - r
                return f"{prefix}{val:g}"
            if left.startswith(prefix) and not right.startswith(('~', '^')):
                val = float(left[1:]) if left[1:] else 0
                val = val + float(right) if op == '+' else val - float(right)
                return f"{prefix}{val:g}"
            if right.startswith(prefix) and not left.startswith(('~', '^')):
                val = float(right[1:]) if right[1:] else 0
                val = float(left) + val if op == '+' else float(left) - val
                return f"{prefix}{val:g}"
        l, r = float(left), float(right)
        val = l + r if op == '+' else l - r
        return f"{val:g}"

    def __add__(self, other: Position | tuple | list | int | float) -> Position:
        other = self._to_position(other)
        return Position(
            self._combine(self._x, other._x, '+'),
            self._combine(self._y, other._y, '+'),
            self._combine(self._z, other._z, '+'),
        )

    def __sub__(self, other: Position | tuple | list | int | float) -> Position:
        other = self._to_position(other)
        return Position(
            self._combine(self._x, other._x, '-'),
            self._combine(self._y, other._y, '-'),
            self._combine(self._z, other._z, '-'),
        )

    def __mul__(self, other: Position | tuple | list | int | float) -> Position:
        other = self._to_position(other)
        def mul(a: str, b: str) -> str:
            prefix = ''
            if a.startswith(('~', '^')):
                prefix = a[0]
                a_val = float(a[1:]) if a[1:] else 1
                b_val = float(b) if not isinstance(b, str) or not b.startswith(('~','^')) else 1
                val = a_val * b_val
                # сохраняем знак
                if val < 0:
                    val = -abs(val)
                return f"{prefix}{val:g}" if val != 0 else prefix
            if b.startswith(('~', '^')):
                prefix = b[0]
                a_val = float(a)
                b_val = float(b[1:]) if b[1:] else 1
                val = a_val * b_val
                if val < 0:
                    val = -abs(val)
                return f"{prefix}{val:g}" if val != 0 else prefix
            return f"{float(a) * float(b):g}"
        return Position(mul(self._x, other._x), mul(self._y, other._y), mul(self._z, other._z))

    def __rmul__(self, other: int | float) -> Position:
        return self * other

    def __truediv__(self, other: Position | tuple | list | int | float) -> Position:
        other = self._to_position(other)
        def div(a: str, b: str) -> str:
            if a.startswith(('~', '^')) or b.startswith(('~', '^')):
                return a if a.startswith(('~', '^')) else b
            return f"{float(a) / float(b):g}"
        return Position(div(self._x, other._x), div(self._y, other._y), div(self._z, other._z))
    
    def __rtruediv__(self, other: int | float) -> Position:
        return self / other

    def distance_to(self, other: Position) -> float:
        """
        Compute Euclidean distance to another Position.

        Args:
            other: target Position

        Returns:
            float: distance
        """
        return math.sqrt(
            (self._to_float(self._x) - self._to_float(other._x)) ** 2 +
            (self._to_float(self._y) - self._to_float(other._y)) ** 2 +
            (self._to_float(self._z) - self._to_float(other._z)) ** 2
        )

    def lerp(self, other: Position, t: float) -> Position:
        """
        Linear interpolation between this position and another.

        Args:
            other: target Position
            t: interpolation factor [0, 1]

        Returns:
            Position: interpolated position
        """
        if not 0 <= t <= 1:
            raise ValueError("t must be in range [0, 1]")
        return Position(
            self._to_float(self._x) + (self._to_float(other._x) - self._to_float(self._x)) * t,
            self._to_float(self._y) + (self._to_float(other._y) - self._to_float(self._y)) * t,
            self._to_float(self._z) + (self._to_float(other._z) - self._to_float(self._z)) * t,
        )

    @classmethod
    def from_tuple(cls, t: tuple[int | float | str, int | float | str, int | float | str]) -> Position:
        """Create a Position from a 3-element tuple."""
        return cls(*t)

Position.VIEW = Position.from_tuple(('^', '^', '^'))
Position.CURRENT = Position.from_tuple(('~', '~', '~'))


if __name__ == '__main__':
    print(Position(1, 2, 3) + Position.VIEW)
    print(Position.VIEW + Position(5))
    print(Position.CURRENT - Position(5, 4))
    print(((Position(1) * Position(5, 2, 8)) + Position.VIEW) * -1)

    pos = Position(5)
    pos.x -= 1
    pos.x *= -1
    pos *= -1
    print(pos)
