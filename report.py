#!/usr/bin/env python3
"""
Report Module - Generates various financial reports and summaries.

This module provides functions for displaying financial summaries,
monthly reports, and transaction lists in a formatted manner.

Author: [Your Name]
Version: 1.0.0
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from storage import load_data
from expense import get_categories, get_expense_summary_by_category

# Month names for display
MONTH_NAMES = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]


def format_currency(amount: float) -> str:
    """
    Format a number as currency.
    
    Args:
        amount: The amount to format.
    
    Returns:
        str: Formatted currency string.
    
    Example:
        >>> print(format_currency(1234.56))
        '$1,234.56'
    """
    return f"${amount:,.2f}"


def display_summary() -> None:
    """
    Display a comprehensive financial summary.
    
    Shows total income, total expenses, current balance,
    and expense breakdown by category.
    
    Returns:
        None
    
    Example:
        >>> display_summary()
        ╔════════════════════════════════════════╗
        ║        FINANCIAL SUMMARY               ║
        ╠════════════════════════════════════════╣
        ...
    """
    data = load_data()
    
    total_income = data.get("total_income", 0.0)
    total_expense = data.get("total_expense", 0.0)
    balance = data.get("balance", 0.0)
    
    # Determine balance status
    if balance > 0:
        balance_status = "✅ POSITIVE"
        balance_color = ""
    elif balance < 0:
        balance_status = "❌ NEGATIVE"
        balance_color = ""
    else:
        balance_status = "⚖️ NEUTRAL"
        balance_color = ""
    
    print()
    print("╔" + "═" * 50 + "╗")
    print("║" + "FINANCIAL SUMMARY".center(50) + "║")
    print("╠" + "═" * 50 + "╣")
    print("║" + " " * 50 + "║")
    print("║  💰 Total Income:    " + f"{format_currency(total_income):>25}" + "   ║")
    print("║  💸 Total Expenses:  " + f"{format_currency(total_expense):>25}" + "   ║")
    print("║" + "─" * 50 + "║")
    print("║  📊 Current Balance: " + f"{format_currency(balance):>25}" + "   ║")
    print("║     Status:          " + f"{balance_status:>25}" + "   ║")
    print("║" + " " * 50 + "║")
    print("╚" + "═" * 50 + "╝")
    
    # Display expense breakdown by category
    print("\n📈 EXPENSE BREAKDOWN BY CATEGORY:")
    print("─" * 45)
    
    category_summary = get_expense_summary_by_category()
    
    if total_expense > 0:
        for category, amount in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
            if amount > 0:
                percentage = (amount / total_expense) * 100
                bar_length = int(percentage / 5)
                bar = "█" * bar_length
                print(f"  {category:<15} {format_currency(amount):>12} ({percentage:5.1f}%) {bar}")
    else:
        print("  No expenses recorded yet.")
    
    print("─" * 45)


def display_monthly_report(month: int, year: int) -> None:
    """
    Display a detailed report for a specific month.
    
    Args:
        month: Month number (1-12).
        year: Year (e.g., 2024).
    
    Returns:
        None
    
    Example:
        >>> display_monthly_report(1, 2024)
        ╔════════════════════════════════════════╗
        ║     MONTHLY REPORT - January 2024      ║
        ...
    """
    data = load_data()
    
    # Filter transactions for the specified month
    monthly_transactions = [
        t for t in data["transactions"]
        if t.get("month") == month and t.get("year") == year
    ]
    
    month_name = MONTH_NAMES[month - 1]
    
    print()
    print("╔" + "═" * 50 + "╗")
    print("║" + f"MONTHLY REPORT - {month_name} {year}".center(50) + "║")
    print("╚" + "═" * 50 + "╝")
    
    if not monthly_transactions:
        print(f"\n📭 No transactions found for {month_name} {year}.")
        return
    
    # Calculate monthly totals
    monthly_income = sum(t["amount"] for t in monthly_transactions if t["type"] == "income")
    monthly_expense = sum(t["amount"] for t in monthly_transactions if t["type"] == "expense")
    monthly_balance = monthly_income - monthly_expense
    
    print(f"\n📊 SUMMARY FOR {month_name.upper()} {year}:")
    print("─" * 45)
    print(f"  💰 Income:   {format_currency(monthly_income):>20}")
    print(f"  💸 Expenses: {format_currency(monthly_expense):>20}")
    print(f"  📊 Net:      {format_currency(monthly_balance):>20}")
    print("─" * 45)
    
    # Display expense breakdown for the month
    print(f"\n📈 EXPENSE BREAKDOWN FOR {month_name.upper()}:")
    print("─" * 45)
    
    # Group expenses by category
    category_totals = {}
    for t in monthly_transactions:
        if t["type"] == "expense":
            category = t.get("category", "Others")
            category_totals[category] = category_totals.get(category, 0) + t["amount"]
    
    if category_totals:
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / monthly_expense) * 100 if monthly_expense > 0 else 0
            bar_length = int(percentage / 5)
            bar = "█" * bar_length
            print(f"  {category:<15} {format_currency(amount):>12} ({percentage:5.1f}%) {bar}")
    else:
        print("  No expenses recorded for this month.")
    
    print("─" * 45)
    
    # Display transaction list
    print(f"\n📝 TRANSACTIONS FOR {month_name.upper()} {year}:")
    print("─" * 70)
    print(f"{'ID':<5} {'Date':<12} {'Type':<10} {'Category':<12} {'Amount':>12} {'Description':<15}")
    print("─" * 70)
    
    for t in sorted(monthly_transactions, key=lambda x: x.get("date", "")):
        t_id = t.get("id", "N/A")
        t_date = t.get("date", "N/A")
        t_type = t.get("type", "N/A").capitalize()
        t_category = t.get("category", "N/A")[:12]
        t_amount = format_currency(t.get("amount", 0))
        t_desc = t.get("description", "")[:15]
        
        # Add indicator for income/expense
        type_indicator = "+" if t["type"] == "income" else "-"
        
        print(f"{t_id:<5} {t_date:<12} {t_type:<10} {t_category:<12} {type_indicator}{t_amount:>11} {t_desc}")
    
    print("─" * 70)
    print(f"Total transactions: {len(monthly_transactions)}")


def display_all_transactions(limit: Optional[int] = None) -> None:
    """
    Display all transactions in a formatted table.
    
    Args:
        limit: Optional maximum number of transactions to display.
               If None, displays all transactions.
    
    Returns:
        None
    
    Example:
        >>> display_all_transactions(10)  # Show last 10 transactions
    """
    data = load_data()
    transactions = data.get("transactions", [])
    
    print()
    print("╔" + "═" * 70 + "╗")
    print("║" + "ALL TRANSACTIONS".center(70) + "║")
    print("╚" + "═" * 70 + "╝")
    
    if not transactions:
        print("\n📭 No transactions found.")
        return
    
    # Sort by date (newest first) and apply limit
    sorted_transactions = sorted(
        transactions,
        key=lambda x: x.get("timestamp", ""),
        reverse=True
    )
    
    if limit:
        sorted_transactions = sorted_transactions[:limit]
        print(f"\n(Showing last {len(sorted_transactions)} transactions)")
    
    print()
    print("─" * 80)
    print(f"{'ID':<5} {'Date':<12} {'Time':<10} {'Type':<10} {'Category':<12} {'Amount':>12} {'Description':<15}")
    print("─" * 80)
    
    for t in sorted_transactions:
        t_id = t.get("id", "N/A")
        t_date = t.get("date", "N/A")
        t_time = t.get("time", "N/A")[:5]  # Show HH:MM only
        t_type = t.get("type", "N/A").capitalize()
        t_category = t.get("category", "N/A")[:12]
        t_amount = format_currency(t.get("amount", 0))
        t_desc = t.get("description", "")[:15]
        
        # Add indicator for income/expense
        type_indicator = "+" if t["type"] == "income" else "-"
        
        print(f"{t_id:<5} {t_date:<12} {t_time:<10} {t_type:<10} {t_category:<12} {type_indicator}{t_amount:>11} {t_desc}")
    
    print("─" * 80)
    print(f"Total: {len(transactions)} transactions | Showing: {len(sorted_transactions)}")


def get_monthly_comparison(year: int) -> List[Dict[str, Any]]:
    """
    Get a comparison of income and expenses for each month of a year.
    
    Args:
        year: The year to analyze.
    
    Returns:
        List[Dict[str, Any]]: List of monthly data with income and expense totals.
    
    Example:
        >>> comparison = get_monthly_comparison(2024)
        >>> print(comparison[0]["month_name"])
        'January'
    """
    data = load_data()
    transactions = data.get("transactions", [])
    
    monthly_data = []
    
    for month in range(1, 13):
        month_transactions = [
            t for t in transactions
            if t.get("month") == month and t.get("year") == year
        ]
        
        income = sum(t["amount"] for t in month_transactions if t["type"] == "income")
        expense = sum(t["amount"] for t in month_transactions if t["type"] == "expense")
        
        monthly_data.append({
            "month": month,
            "month_name": MONTH_NAMES[month - 1],
            "income": round(income, 2),
            "expense": round(expense, 2),
            "net": round(income - expense, 2),
            "transaction_count": len(month_transactions)
        })
    
    return monthly_data


def display_yearly_report(year: int) -> None:
    """
    Display a yearly summary report.
    
    Args:
        year: The year to report on.
    
    Returns:
        None
    
    Example:
        >>> display_yearly_report(2024)
    """
    monthly_data = get_monthly_comparison(year)
    
    print()
    print("╔" + "═" * 70 + "╗")
    print("║" + f"YEARLY REPORT - {year}".center(70) + "║")
    print("╚" + "═" * 70 + "╝")
    
    print()
    print("─" * 70)
    print(f"{'Month':<12} {'Income':>15} {'Expenses':>15} {'Net':>15} {'Txns':>8}")
    print("─" * 70)
    
    total_income = 0
    total_expense = 0
    total_transactions = 0
    
    for month_data in monthly_data:
        income = month_data["income"]
        expense = month_data["expense"]
        net = month_data["net"]
        txn_count = month_data["transaction_count"]
        
        total_income += income
        total_expense += expense
        total_transactions += txn_count
        
        if txn_count > 0:
            net_indicator = "+" if net >= 0 else ""
            print(f"{month_data['month_name']:<12} {format_currency(income):>15} {format_currency(expense):>15} {net_indicator}{format_currency(net):>14} {txn_count:>8}")
    
    print("─" * 70)
    net_total = total_income - total_expense
    net_indicator = "+" if net_total >= 0 else ""
    print(f"{'TOTAL':<12} {format_currency(total_income):>15} {format_currency(total_expense):>15} {net_indicator}{format_currency(net_total):>14} {total_transactions:>8}")
    print("─" * 70)