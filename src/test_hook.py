"""Test module for pre-commit hook functionality."""
from typing import Union, Optional

def some_function() -> None:
    """Demonstrate a function that follows good practices."""
    # Implementation can go here
    pass

def add_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers together.
    
    Args:
        a: First number to add
        b: Second number to add
        
    Returns:
        The sum of a and b
    """
    return a + b

# Example usage with proper type safety
result = add_numbers(5, 10)  # Now using proper numeric types