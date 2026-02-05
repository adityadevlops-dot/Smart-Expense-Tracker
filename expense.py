#!/usr/bin/env python3
"""
Expense Module - Handles income and expense operations.

This module provides functions for adding income and expenses,
managing categories, and creating transaction records.

Author: [Your Name]
Version: 1.0.0
"""

from datetime import datetime
from typing import Tuple, List, Dict, Any
import uuid
import numbers
from storage import load_data, save_data


# Predefined expense categories
EXPENSE_CATEGORIES = [
    "Food",
    "Travel",
    "Rent",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Shopping",
    "Education",
    "Others"
]


def get_categories() -> List[str]:
    """
    Get the list of available expense categories.
    
    Returns:
        List[str]: List of expense category names.
    
    Example:
        >>> categories = get_categories()
        >>> print(categories[0])
        'Food'
    """
    return EXPENSE_CATEGORIES.copy()


def generate_transaction_id(transactions: List[Dict]) -> str:
    """
    Generate a unique transaction ID using UUID.
    
    This approach avoids race conditions (TOCTOU) and collisions from deleted entries.
    
    Args:
        transactions: List of existing transactions (not used, kept for compatibility).
    
    Returns:
        str: A universally unique transaction ID string.
    
    Example:
        >>> new_id = generate_transaction_id([])
        >>> print(isinstance(new_id, str))
        True
    """
    return str(uuid.uuid4())


def create_transaction(
    amount: float,
    transaction_type: str,
    category: str,
    description: str
) -> Dict[str, Any]:
    """
    Create a new transaction dictionary.
    
    Args:
        amount: Transaction amount (positive float).
        transaction_type: Either "income" or "expense".
        category: Category of the transaction.
        description: Description of the transaction.
    
    Returns:
        Dict[str, Any]: Transaction dictionary with all fields.
    
    Example:
        >>> trans = create_transaction(100.0, "income", "Salary", "Monthly salary")
        >>> print(trans["type"])
        'income'
    """
    now = datetime.now()
    
    return {
        "id": 0,  # Will be set when saving
        "type": transaction_type,
        "amount": round(amount, 2),
        "category": category,
        "description": description,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "month": now.month,
        "year": now.year,
        "timestamp": now.isoformat()
    }


def add_income(amount: float, description: str = "Income") -> Tuple[bool, str]:
    """
    Add an income entry to the tracker.
    
    Args:
        amount: Income amount (must be positive).
        description: Description of the income source.
    
    Returns:
        Tuple[bool, str]: (Success status, Message)
    
    Example:
        >>> success, msg = add_income(5000.00, "Monthly Salary")
        >>> print(success)
        True
    """
    # Validate amount is numeric (exclude booleans)
    if isinstance(amount, bool) or not isinstance(amount, numbers.Real):
        return False, "Amount must be a numeric value greater than zero."
    
    # Validate amount is positive
    if amount <= 0:
        return False, "Amount must be greater than zero."
    
    # Load existing data
    data = load_data()
    
    # Create transaction
    transaction = create_transaction(
        amount=amount,
        transaction_type="income",
        category="Income",
        description=description
    )
    
    # Assign unique ID
    transaction["id"] = generate_transaction_id(data["transactions"])
    
    # Add to transactions list
    data["transactions"].append(transaction)
    
    # Update totals
    data["total_income"] = round(data["total_income"] + amount, 2)
    data["balance"] = round(data["total_income"] - data["total_expense"], 2)
    
    # Save data
    if save_data(data):
        return True, f"Income of ${amount:.2f} added successfully!"
    else:
        return False, "Failed to save data."


def add_expense(
    amount: float,
    category: str,
    description: str = "Expense"
) -> Tuple[bool, str]:
    """
    Add an expense entry to the tracker.
    
    Args:
        amount: Expense amount (must be positive).
        category: Expense category (must be valid).
        description: Description of the expense.
    
    Returns:
        Tuple[bool, str]: (Success status, Message)
    
    Example:
        >>> success, msg = add_expense(50.00, "Food", "Groceries")
        >>> print(success)
        True
    """
    # Validate amount is numeric (exclude booleans)
    if isinstance(amount, bool) or not isinstance(amount, numbers.Real):
        return False, "Amount must be a numeric value greater than zero."
    
    # Validate amount is positive
    if amount <= 0:
        return False, "Amount must be greater than zero."
    
    # Validate category
    if category not in EXPENSE_CATEGORIES:
        return False, f"Invalid category. Choose from: {', '.join(EXPENSE_CATEGORIES)}"
    
    # Load existing data
    data = load_data()
    
    # Create transaction
    transaction = create_transaction(
        amount=amount,
        transaction_type="expense",
        category=category,
        description=description
    )
    
    # Assign unique ID
    transaction["id"] = generate_transaction_id(data["transactions"])
    
    # Add to transactions list
    data["transactions"].append(transaction)
    
    # Update totals
    data["total_expense"] = round(data["total_expense"] + amount, 2)
    data["balance"] = round(data["total_income"] - data["total_expense"], 2)
    
    # Save data
    if save_data(data):
        return True, f"Expense of ${amount:.2f} ({category}) added successfully!"
    else:
        return False, "Failed to save data."


def get_transactions_by_type(transaction_type: str) -> List[Dict[str, Any]]:
    """
    Get all transactions of a specific type.
    
    Args:
        transaction_type: Either "income" or "expense".
    
    Returns:
        List[Dict[str, Any]]: List of matching transactions.
    
    Example:
        >>> expenses = get_transactions_by_type("expense")
        >>> print(len(expenses))
        5
    """
    data = load_data()
    return [t for t in data["transactions"] if t["type"] == transaction_type]


def get_transactions_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Get all transactions of a specific category.
    
    Args:
        category: The category to filter by.
    
    Returns:
        List[Dict[str, Any]]: List of matching transactions.
    
    Example:
        >>> food_expenses = get_transactions_by_category("Food")
        >>> print(len(food_expenses))
        3
    """
    data = load_data()
    return [t for t in data["transactions"] if t["category"] == category]


def get_transactions_by_month(month: int, year: int) -> List[Dict[str, Any]]:
    """
    Get all transactions for a specific month and year.
    
    Args:
        month: Month number (1-12).
        year: Year (e.g., 2024).
    
    Returns:
        List[Dict[str, Any]]: List of matching transactions.
    
    Example:
        >>> jan_transactions = get_transactions_by_month(1, 2024)
        >>> print(len(jan_transactions))
        10
    """
    data = load_data()
    return [
        t for t in data["transactions"]
        if t["month"] == month and t["year"] == year
    ]


def delete_transaction(transaction_id: int) -> Tuple[bool, str]:
    """
    Delete a transaction by its ID.
    
    Args:
        transaction_id: The unique ID of the transaction to delete.
    
    Returns:
        Tuple[bool, str]: (Success status, Message)
    
    Example:
        >>> success, msg = delete_transaction(1)
        >>> print(success)
        True
    """
    data = load_data()
    
    # Find the transaction
    transaction = None
    for t in data["transactions"]:
        if t["id"] == transaction_id:
            transaction = t
            break
    
    if transaction is None:
        return False, f"Transaction with ID {transaction_id} not found."
    
    # Remove from list
    data["transactions"].remove(transaction)
    
    # Update totals
    if transaction["type"] == "income":
        data["total_income"] = round(data["total_income"] - transaction["amount"], 2)
    else:
        data["total_expense"] = round(data["total_expense"] - transaction["amount"], 2)
    
    data["balance"] = round(data["total_income"] - data["total_expense"], 2)
    
    # Save data
    if save_data(data):
        return True, f"Transaction ID {transaction_id} deleted successfully!"
    else:
        return False, "Failed to save data."


def get_expense_summary_by_category() -> Dict[str, float]:
    """
    Get a summary of expenses grouped by category.
    
    Returns:
        Dict[str, float]: Dictionary with category names as keys and total amounts as values.
    
    Example:
        >>> summary = get_expense_summary_by_category()
        >>> print(summary["Food"])
        150.00
    """
    data = load_data()
    summary = {category: 0.0 for category in EXPENSE_CATEGORIES}
    
    for t in data["transactions"]:
        if t["type"] == "expense" and t["category"] in summary:
            summary[t["category"]] += t["amount"]
    
    # Round all values
    return {k: round(v, 2) for k, v in summary.items()}