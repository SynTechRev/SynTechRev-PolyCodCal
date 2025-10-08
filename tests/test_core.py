from syntechrev_polycodcal.core import greet


def test_greet_no_name():
    assert greet() == "Hello, world!"


def test_greet_with_name():
    assert greet("Alice") == "Hello, Alice!"
