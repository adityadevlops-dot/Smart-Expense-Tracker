#!/usr/bin/env python3
"""
Visualization Module - Generates charts and graphs for expense data.

This module provides functions for creating visual representations
of financial data using matplotlib.

Author: [Your Name]
Version: 1.0.0
"""

import os
from typing import Optional, Tuple, Dict, List
from datetime import datetime

# Try to import matplotlib
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from storage import load_data
from expense import get_categories, get_expense_summary_by_category
from report import MONTH_NAMES


def check_matplotlib() -> bool:
    """
    Check if matplotlib is available.
    
    Returns:
        bool: True if matplotlib is installed, False otherwise.
    """
    return MATPLOTLIB_AVAILABLE


def generate_expense_chart(
    month: Optional[int] = None,
    year: Optional[int] = None,
    save_path: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Generate a bar chart showing expenses by category.
    
    Args:
        month: Optional month filter (1-12). If None, shows all months.
        year: Year to filter by.
        save_path: Optional custom path to save the chart image.
    
    Returns:
        Tuple[bool, str]: (Success status, Message)
    
    Example:
        >>> success, msg = generate_expense_chart(1, 2024)
        >>> print(msg)
        'Chart saved as expense_chart_2024_01.png'
    """
    if not MATPLOTLIB_AVAILABLE:
        return False, "matplotlib is not installed. Install it using: pip install matplotlib"
    
    data = load_data()
    transactions = data.get("transactions", [])
    
    if not transactions:
        return False, "No transactions to visualize."
    
    # Filter transactions
    if year is None:
        year = datetime.now().year
    
    if month is not None:
        filtered = [
            t for t in transactions
            if t.get("type") == "expense" and t.get("month") == month and t.get("year") == year
        ]
        title_period = f"{MONTH_NAMES[month - 1]} {year}"
    else:
        filtered = [
            t for t in transactions
            if t.get("type") == "expense" and t.get("year") == year
        ]
        title_period = f"Year {year}"
    
    if not filtered:
        return False, f"No expense data found for {title_period}."
    
    # Calculate totals by category
    category_totals: Dict[str, float] = {}
    for t in filtered:
        category = t.get("category", "Others")
        category_totals[category] = category_totals.get(category, 0) + t.get("amount", 0)
    
    # Sort by value
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    categories = [c[0] for c in sorted_categories]
    amounts = [c[1] for c in sorted_categories]
    
    # Define colors for categories
    colors = [
        '#FF6B6B',  # Red
        '#4ECDC4',  # Teal
        '#45B7D1',  # Blue
        '#96CEB4',  # Green
        '#FFEAA7',  # Yellow
        '#DDA0DD',  # Plum
        '#98D8C8',  # Mint
        '#F7DC6F',  # Gold
        '#BB8FCE',  # Purple
    ]
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f'Expense Analysis - {title_period}', fontsize=16, fontweight='bold')
    
    # Bar chart
    bars = ax1.bar(categories, amounts, color=colors[:len(categories)], edgecolor='white', linewidth=1.2)
    ax1.set_xlabel('Category', fontsize=12)
    ax1.set_ylabel('Amount ($)', fontsize=12)
    ax1.set_title('Expenses by Category', fontsize=14)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, amount in zip(bars, amounts):
        height = bar.get_height()
        ax1.annotate(f'${amount:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)
    
    # Pie chart
    if sum(amounts) > 0:
        wedges, texts, autotexts = ax2.pie(
            amounts,
            labels=categories,
            autopct='%1.1f%%',
            colors=colors[:len(categories)],
            startangle=90,
            explode=[0.02] * len(categories)
        )
        ax2.set_title('Expense Distribution', fontsize=14)
        
        # Improve label readability
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
    
    # Adjust layout
    plt.tight_layout()
    
    # Generate filename
    if save_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if month is not None:
            filename = f"expense_chart_{year}_{month:02d}.png"
        else:
            filename = f"expense_chart_{year}.png"
        save_path = os.path.join(script_dir, filename)
    
    # Save the chart
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return True, f"Chart saved as {os.path.basename(save_path)}"


def generate_monthly_trend_chart(
    year: int,
    save_path: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Generate a line chart showing monthly income vs expense trends.
    
    Args:
        year: Year to analyze.
        save_path: Optional custom path to save the chart image.
    
    Returns:
        Tuple[bool, str]: (Success status, Message)
    
    Example:
        >>> success, msg = generate_monthly_trend_chart(2024)
        >>> print(msg)
        'Trend chart saved as monthly_trend_2024.png'
    """
    if not MATPLOTLIB_AVAILABLE:
        return False, "matplotlib is not installed. Install it using: pip install matplotlib"
    
    data = load_data()
    transactions = data.get("transactions", [])
    
    if not transactions:
        return False, "No transactions to visualize."
    
    # Calculate monthly totals
    monthly_income = [0.0] * 12
    monthly_expense = [0.0] * 12
    
    for t in transactions:
        if t.get("year") == year:
            month_idx = t.get("month", 1) - 1
            if t.get("type") == "income":
                monthly_income[month_idx] += t.get("amount", 0)
            else:
                monthly_expense[month_idx] += t.get("amount", 0)
    
    # Check if there's any data
    if sum(monthly_income) == 0 and sum(monthly_expense) == 0:
        return False, f"No data found for year {year}."
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    months = [m[:3] for m in MONTH_NAMES]  # Abbreviated month names
    x = range(12)
    
    # Plot lines
    ax.plot(x, monthly_income, 'g-o', label='Income', linewidth=2, markersize=8)
    ax.plot(x, monthly_expense, 'r-o', label='Expenses', linewidth=2, markersize=8)
    
    # Calculate and plot net
    monthly_net = [inc - exp for inc, exp in zip(monthly_income, monthly_expense)]
    ax.plot(x, monthly_net, 'b--', label='Net', linewidth=1.5, alpha=0.7)
    
    # Fill areas
    ax.fill_between(x, monthly_income, alpha=0.3, color='green')
    ax.fill_between(x, monthly_expense, alpha=0.3, color='red')
    
    # Customize chart
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Amount ($)', fontsize=12)
    ax.set_title(f'Monthly Income vs Expenses Trend - {year}', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(months)
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add value annotations for non-zero values
    for i, (inc, exp) in enumerate(zip(monthly_income, monthly_expense)):
        if inc > 0:
            ax.annotate(f'${inc:.0f}', (i, inc), textcoords="offset points",
                       xytext=(0, 10), ha='center', fontsize=8, color='green')
        if exp > 0:
            ax.annotate(f'${exp:.0f}', (i, exp), textcoords="offset points",
                       xytext=(0, -15), ha='center', fontsize=8, color='red')
    
    plt.tight_layout()
    
    # Generate filename
    if save_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = f"monthly_trend_{year}.png"
        save_path = os.path.join(script_dir, filename)
    
    # Save the chart
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return True, f"Trend chart saved as {os.path.basename(save_path)}"


def generate_category_comparison_chart(
    months: List[int],
    year: int,
    save_path: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Generate a grouped bar chart comparing categories across multiple months.
    
    Args:
        months: List of months to compare.
        year: Year to analyze.
        save_path: Optional custom path to save the chart image.
    
    Returns:
        Tuple[bool, str]: (Success status, Message)
    """
    if not MATPLOTLIB_AVAILABLE:
        return False, "matplotlib is not installed."
    
    data = load_data()
    transactions = data.get("transactions", [])
    
    if not transactions:
        return False, "No transactions to visualize."
    
    categories = get_categories()
    
    # Calculate totals for each month and category
    month_data = {}
    for month in months:
        month_data[month] = {cat: 0.0 for cat in categories}
        for t in transactions:
            if (t.get("type") == "expense" and 
                t.get("month") == month and 
                t.get("year") == year):
                cat = t.get("category", "Others")
                if cat in month_data[month]:
                    month_data[month][cat] += t.get("amount", 0)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))
    
    x = range(len(categories))
    width = 0.8 / len(months)
    
    colors = plt.cm.Set3(range(len(months)))
    
    for i, month in enumerate(months):
        offset = (i - len(months) / 2 + 0.5) * width
        values = [month_data[month][cat] for cat in categories]
        bars = ax.bar([xi + offset for xi in x], values, width, 
                     label=MONTH_NAMES[month - 1], color=colors[i])
    
    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('Amount ($)', fontsize=12)
    ax.set_title(f'Category Comparison - {year}', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    
    # Generate filename
    if save_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        month_str = "_".join([str(m) for m in months])
        filename = f"category_comparison_{year}_{month_str}.png"
        save_path = os.path.join(script_dir, filename)
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return True, f"Comparison chart saved as {os.path.basename(save_path)}"