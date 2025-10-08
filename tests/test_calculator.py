"""Tests for calculator module."""

import pytest
from syntechrev_polycodcal.calculator import add, subtract, multiply, divide


class TestAdd:
    """Tests for add function."""

    def test_add_positive_numbers(self):
        """Test adding positive numbers."""
        assert add(2, 3) == 5
        assert add(10, 20) == 30

    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        assert add(-2, -3) == -5
        assert add(-10, -20) == -30

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert add(5, -3) == 2
        assert add(-5, 3) == -2

    def test_add_zero(self):
        """Test adding zero."""
        assert add(0, 5) == 5
        assert add(5, 0) == 5
        assert add(0, 0) == 0


class TestSubtract:
    """Tests for subtract function."""

    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        assert subtract(5, 3) == 2
        assert subtract(20, 10) == 10

    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers."""
        assert subtract(-5, -3) == -2
        assert subtract(-10, -20) == 10

    def test_subtract_mixed_numbers(self):
        """Test subtracting mixed numbers."""
        assert subtract(5, -3) == 8
        assert subtract(-5, 3) == -8

    def test_subtract_zero(self):
        """Test subtracting zero."""
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5


class TestMultiply:
    """Tests for multiply function."""

    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        assert multiply(2, 3) == 6
        assert multiply(10, 5) == 50

    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        assert multiply(-2, -3) == 6
        assert multiply(-10, -5) == 50

    def test_multiply_mixed_numbers(self):
        """Test multiplying mixed numbers."""
        assert multiply(2, -3) == -6
        assert multiply(-2, 3) == -6

    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        assert multiply(5, 0) == 0
        assert multiply(0, 5) == 0
        assert multiply(0, 0) == 0


class TestDivide:
    """Tests for divide function."""

    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        assert divide(6, 3) == 2
        assert divide(10, 5) == 2

    def test_divide_negative_numbers(self):
        """Test dividing negative numbers."""
        assert divide(-6, -3) == 2
        assert divide(-10, -5) == 2

    def test_divide_mixed_numbers(self):
        """Test dividing mixed numbers."""
        assert divide(6, -3) == -2
        assert divide(-6, 3) == -2

    def test_divide_by_zero(self):
        """Test dividing by zero raises error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)

    def test_divide_zero(self):
        """Test dividing zero."""
        assert divide(0, 5) == 0
