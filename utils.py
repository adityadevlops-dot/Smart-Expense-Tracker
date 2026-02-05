#!/usr/bin/env python3
"""
Utilities Module - Helper functions for the expense tracker.

This module provides utility functions for input validation,
formatting, file operations, and user interface helpers.

Author: [Your Name]
Version: 1.0.0
"""

import os
import sys
import csv
from typing import Optional, Union, List, Dict, Any, Tuple
from datetime import datetime


def clear_screen() -> None:
    """
    Clear the console screen.
    
    Works on both Windows and Unix-like systems.
    
    Returns:
        None
    
    Example:
        >>> clear_screen()
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str, width: int = 50) -> None:
    """
    Print a formatted header with a title.
    
    Args:
        title: The title text to display.
        width: Width of the header box.
    
    Returns:
        None
    
    Example:
        >>> print_header("ADD EXPENSE")
        ╔══════════════════════════════════════════════════╗
        ║                   ADD EXPENSE                    ║
        ╚══════════════════════════════════════════════════╝
    """
    print()
    print("╔" + "═" * width + "╗")
    print("║" + title.center(width) + "║")
    print("╚" + "═" * width + "╝")
    print()


def print_menu(title: str, options: List[str]) -> None:
    """
    Print a formatted menu with numbered options.
    
    Args:
        title: The menu title.
        options: List of menu option strings.
    
    Returns:
        None
    
    Example:
        >>> print_menu("MAIN MENU", ["Option 1", "Option 2", "Exit"])
    """
    print()
    print("┌" + "─" * 40 + "┐")
    print("│" + title.center(40) + "│")
    print("├" + "─" * 40 + "┤")
    
    for idx, option in enumerate(options, 1):
        option_text = f"  {idx}. {option}"
        print("│" + option_text.ljust(40) + "│")
    
    print("└" + "─" * 40 + "┘")


def get_valid_input(
    prompt: str,
    input_type: str = "str",
    min_value: Optional[Union[int, float]] = None,
    max_value: Optional[Union[int, float]] = None,
    allowed_values: Optional[List[Any]] = None,
    allow_empty: bool = False
) -> Optional[Union[str, int, float]]:
    """
    Get validated input from the user.
    
    Args:
        prompt: The prompt to display to the user.
        input_type: Type of input expected ("str", "int", "float").
        min_value: Minimum allowed value for numeric inputs.
        max_value: Maximum allowed value for numeric inputs.
        allowed_values: List of allowed values for the input.
        allow_empty: Whether to allow empty input.
    
    Returns:
        Optional[Union[str, int, float]]: The validated input, or None if invalid.
    
    Example:
        >>> amount = get_valid_input("Enter amount: ", "float", min_value=0.01)
        Enter amount: 50.00
        >>> print(amount)
        50.0
    """
    try:
        user_input = input(prompt).strip()
        
        if not user_input:
            if allow_empty:
                return ""
            return None
        
        if input_type == "int":
            value = int(user_input)
        elif input_type == "float":
            value = float(user_input)
        else:
            value = user_input
        
        # Check min value
        if min_value is not None and isinstance(value, (int, float)):
            if value < min_value:
                return None
        
        # Check max value
        if max_value is not None and isinstance(value, (int, float)):
            if value > max_value:
                return None
        
        # Check allowed values
        if allowed_values is not None:
            if value not in allowed_values:
                return None
        
        return value
    
    except ValueError:
        return None
    except KeyboardInterrupt:
        print("\n")
        return None


def pause() -> None:
    """
    Pause execution and wait for user to press Enter.
    
    Returns:
        None
    
    Example:
        >>> pause()
        Press Enter to continue...
    """
    try:
        input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        print("\n")


def format_date(date_str: str, input_format: str = "%Y-%m-%d", output_format: str = "%B %d, %Y") -> str:
    """
    Format a date string from one format to another.
    
    Args:
        date_str: The date string to format.
        input_format: The format of the input date string.
        output_format: The desired output format.
    
    Returns:
        str: The formatted date string.
    
    Example:
        >>> print(format_date("2024-01-15"))
        'January 15, 2024'
    """
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except ValueError:
        return date_str


def export_to_csv(filename: str = "expenses.csv") -> Tuple[bool, str]:
    """
    Export all transactions to a CSV file.
    
    Args:
        filename: Name of the CSV file to create.
    
    Returns:
        Tuple[bool, str]: (Success status, Message)
    
    Example:
        >>> success, message = export_to_csv("my_expenses.csv")
        >>> print(message)
        'Data exported to my_expenses.csv successfully!'
    """
    from storage import load_data
    
    try:
        data = load_data()
        transactions = data.get("transactions", [])
        
        if not transactions:
            return False, "No transactions to export."
        
        # Define CSV columns
        fieldnames = [
            "ID", "Date", "Time", "Type", "Category",
            "Amount", "Description", "Month", "Year"
        ]
        
        # Get the directory of the main script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for t in transactions:
                writer.writerow({
                    "ID": t.get("id", ""),
                    "Date": t.get("date", ""),
                    "Time": t.get("time", ""),
                    "Type": t.get("type", "").capitalize(),
                    "Category": t.get("category", ""),
                    "Amount": t.get("amount", 0),
                    "Description": t.get("description", ""),
                    "Month": t.get("month", ""),
                    "Year": t.get("year", "")
                })
        
        return True, f"Data exported to {filename} successfully! ({len(transactions)} transactions)"
    
    except IOError as e:
        return False, f"Error exporting to CSV: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> bool:
    """
    Validate if a string is a valid date.
    
    Args:
        date_str: The date string to validate.
        date_format: The expected date format.
    
    Returns:
        bool: True if valid date, False otherwise.
    
    Example:
        >>> validate_date("2024-01-15")
        True
        >>> validate_date("invalid-date")
        False
    """
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def get_current_month_year() -> Tuple[int, int]:
    """
    Get the current month and year.
    
    Returns:
        Tuple[int, int]: (month, year)
    
    Example:
        >>> month, year = get_current_month_year()
        >>> print(month, year)
        1 2024
    """
    now = datetime.now()
    return now.month, now.year


def format_number(number: float, decimal_places: int = 2) -> str:
    """
    Format a number with thousand separators and decimal places.
    
    Args:
        number: The number to format.
        decimal_places: Number of decimal places.
    
    Returns:
        str: Formatted number string.
    
    Example:
        >>> print(format_number(1234567.89))
        '1,234,567.89'
    """
    return f"{number:,.{decimal_places}f}"


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length with a suffix.
    
    Args:
        text: The string to truncate.
        max_length: Maximum length including suffix.
        suffix: The suffix to add if truncated.
    
    Returns:
        str: Truncated string.
    
    Example:
        >>> print(truncate_string("This is a long description", 15))
        'This is a lo...'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def confirm_action(prompt: str = "Are you sure?") -> bool:
    """
    Ask for user confirmation.
    
    Args:
        prompt: The confirmation prompt to display.
    
    Returns:
        bool: True if user confirms, False otherwise.
    
    Example:
        >>> if confirm_action("Delete this transaction?"):
        ...     print("Deleted!")
    """
    try:
        response = input(f"{prompt} (y/n): ").strip().lower()
        return response in ('y', 'yes')
    except KeyboardInterrupt:
        print("\n")
        return False


def print_success(message: str) -> None:
    """
    Print a success message with formatting.
    
    Args:
        message: The success message to display.
    
    Returns:
        None
    """
    print(f"\n✅ {message}")


def print_error(message: str) -> None:
    """
    Print an error message with formatting.
    
    Args:
        message: The error message to display.
    
    Returns:
        None
    """
    print(f"\n❌ {message}")


def print_warning(message: str) -> None:
    """
    Print a warning message with formatting.
    
    Args:
        message: The warning message to display.
    
    Returns:
        None
    """
    print(f"\n⚠️ {message}")


def print_info(message: str) -> None:
    """
    Print an info message with formatting.
    
    Args:
        message: The info message to display.
    
    Returns:
        None
    """
    print(f"\nℹ️ {message}")