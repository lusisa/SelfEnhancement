"""Utility functions for MyPackage.

This module contains helper functions for common operations.
"""

from typing import Union


def greet(name: str) -> str:
    """Generate a greeting message.
    
    Args:
        name: The name of the person to greet.
        
    Returns:
        A greeting string.
        
    Examples:
        >>> greet("Alice")
        'Hello, Alice!'
    """
    return f"Hello, {name}!"


def add_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers together.
    
    Args:
        a: The first number.
        b: The second number.
        
    Returns:
        The sum of a and b.
        
    Examples:
        >>> add_numbers(2, 3)
        5
        >>> add_numbers(2.5, 3.5)
        6.0
    """
    return a + b


def is_even(number: int) -> bool:
    """Check if a number is even.
    
    Args:
        number: The integer to check.
        
    Returns:
        True if the number is even, False otherwise.
        
    Examples:
        >>> is_even(4)
        True
        >>> is_even(7)
        False
    """
    return number % 2 == 0
