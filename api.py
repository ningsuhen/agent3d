"""
String Manipulation Utility Module

This module provides utility functions for common string manipulation operations
following Domain-Driven Design principles.

Functions:
    reverse(text: str) -> str: Returns the reversed version of input text
    capitalize(text: str) -> str: Returns text with first letter of each word capitalized
    word_count(text: str) -> int: Returns the number of words in the text
"""

from typing import Optional


def reverse(text: str) -> str:
    """
    Reverses the input text.

    Args:
        text (str): The input text to be reversed

    Returns:
        str: The reversed text

    Examples:
        >>> reverse("hello")
        'olleh'
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return text[::-1]


def capitalize(text: str) -> str:
    """
    Capitalizes the first letter of each word in the text.

    Args:
        text (str): The input text to be capitalized

    Returns:
        str: Text with first letter of each word capitalized

    Examples:
        >>> capitalize("hello world")
        'Hello World'
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return text.title()


def word_count(text: str, ignore_empty: bool = True) -> int:
    """
    Counts the number of words in the text.

    Args:
        text (str): The input text to count words from
        ignore_empty (bool, optional): If True, ignores empty strings between spaces.
                                     Defaults to True.

    Returns:
        int: Number of words in the text

    Examples:
        >>> word_count("hello world")
        2
        >>> word_count("hello   world", ignore_empty=True)
        2
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    if ignore_empty:
        # Split and automatically filter out empty strings
        return len(text.split())
    else:
        # Split by space and keep empty strings between multiple spaces
        return len(text.split(' '))