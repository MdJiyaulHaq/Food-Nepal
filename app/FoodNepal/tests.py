from . import calculator


def test_add():
    assert calculator.add(a=1, b=2, c=3) == 6
    assert calculator.add(x=10, y=20) == 30
    assert calculator.add() == 0
