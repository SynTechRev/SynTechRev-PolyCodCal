from syntechrev_polycodcal.core import greet


def test_greet_no_name():
    assert greet() == "Hello, world!"


def test_greet_with_name():
    assert greet("Alice") == "Hello, Alice!"


def test_greet_empty_string():
    # empty string should be treated as no name
    assert greet("") == "Hello, world!"


def test_greet_whitespace_name():
    # whitespace-only name is considered non-empty by current logic, ensure behavior
    assert greet("  ") == "Hello,   !"


def test_greet_none_explicit():
    assert greet(None) == "Hello, world!"
