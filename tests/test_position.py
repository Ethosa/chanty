from chanty import Position


def test_addition():
    assert str(Position.VIEW + Position(1, 2, 3)) == "^1 ^2 ^3"


def test_subtraction():
    assert str(Position.CURRENT - Position(2, 0, 5)) == "~-2 ~-0 ~-5"


def test_multiplication():
    assert str(Position(2) * Position(10, 20, "~")) == "20 40 ~2"
