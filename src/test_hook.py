import sys
import os

def some_function():
    unused_var = "test"  # This will trigger a pylint warning
    x = 5  # This will trigger a warning about single-character variable names
    return None  # This will trigger a warning about explicit return of None

# This will trigger a type checking warning
def add_numbers(a, b):
    return a + b

result = add_numbers("5", 10)  # Type mismatch that mypy should catch