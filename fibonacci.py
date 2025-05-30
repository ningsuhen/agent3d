"""
Fibonacci number calculator module.

This module provides functionality to calculate Fibonacci numbers efficiently
using an iterative approach. It includes input validation and example usage.
"""

def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    
    The Fibonacci sequence is defined as:
    - F(0) = 0
    - F(1) = 1
    - F(n) = F(n-1) + F(n-2) for n > 1
    
    Args:
        n: A non-negative integer representing the position in the Fibonacci sequence.
        
    Returns:
        The nth Fibonacci number.
        
    Raises:
        ValueError: If n is negative.
        TypeError: If n is not an integer.
    """
    # Input validation
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be non-negative")
    
    # Handle base cases
    if n <= 1:
        return n
    
    # Calculate Fibonacci number iteratively
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    # Example usage
    try:
        # Calculate and print first 10 Fibonacci numbers
        print("First 10 Fibonacci numbers:")
        for i in range(10):
            print(f"F({i}) = {fibonacci(i)}")
        
        # Example with error handling
        print("\nTrying with invalid input:")
        print(fibonacci(-1))  # This will raise ValueError
    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")