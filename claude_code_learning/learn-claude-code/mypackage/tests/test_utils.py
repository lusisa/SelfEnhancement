"""Unit tests for utils module.

This module contains test cases for the utility functions.
"""

import unittest
from mypackage.utils import greet, add_numbers, is_even


class TestGreet(unittest.TestCase):
    """Test cases for the greet function."""
    
    def test_greet_simple_name(self) -> None:
        """Test greeting with a simple name."""
        result = greet("Alice")
        self.assertEqual(result, "Hello, Alice!")
    
    def test_greet_empty_string(self) -> None:
        """Test greeting with an empty string."""
        result = greet("")
        self.assertEqual(result, "Hello, !")
    
    def test_greet_with_spaces(self) -> None:
        """Test greeting with a name containing spaces."""
        result = greet("John Doe")
        self.assertEqual(result, "Hello, John Doe!")


class TestAddNumbers(unittest.TestCase):
    """Test cases for the add_numbers function."""
    
    def test_add_integers(self) -> None:
        """Test adding two integers."""
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)
    
    def test_add_floats(self) -> None:
        """Test adding two floats."""
        result = add_numbers(2.5, 3.5)
        self.assertEqual(result, 6.0)
    
    def test_add_integer_and_float(self) -> None:
        """Test adding an integer and a float."""
        result = add_numbers(2, 3.5)
        self.assertEqual(result, 5.5)
    
    def test_add_negative_numbers(self) -> None:
        """Test adding negative numbers."""
        result = add_numbers(-5, -3)
        self.assertEqual(result, -8)
    
    def test_add_zero(self) -> None:
        """Test adding zero."""
        result = add_numbers(5, 0)
        self.assertEqual(result, 5)


class TestIsEven(unittest.TestCase):
    """Test cases for the is_even function."""
    
    def test_even_number(self) -> None:
        """Test with an even number."""
        result = is_even(4)
        self.assertTrue(result)
    
    def test_odd_number(self) -> None:
        """Test with an odd number."""
        result = is_even(7)
        self.assertFalse(result)
    
    def test_zero(self) -> None:
        """Test with zero (which is even)."""
        result = is_even(0)
        self.assertTrue(result)
    
    def test_negative_even_number(self) -> None:
        """Test with a negative even number."""
        result = is_even(-6)
        self.assertTrue(result)
    
    def test_negative_odd_number(self) -> None:
        """Test with a negative odd number."""
        result = is_even(-3)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
