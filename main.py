#!/usr/bin/env python3
"""
Smart Expense Tracker - Main Application Entry Point

A professional console-based expense tracking application
that helps users manage their income and expenses effectively.

Author: [Aditya Kumar Chaubey]
Version: 1.0.0
"""

import sys
from expense import add_income, add_expense, get_categories
from storage import initialize_data_file, load_data
from report import (
    display_summary,
    display_monthly_report,
    display_all_transactions
)
from utils import (
    clear_screen,
    print_header,
    print_menu,
    get_valid_input,
    pause,
    export_to_csv
)

# Try to import visualization module (optional dependency)
try:
    from visualization import generate_expense_chart
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False


def display_main_menu():
    """
    Display the main menu options to the user.
    
    Returns:
        None
    """
    menu_options = [
        "Add Income",
        "Add Expense",
        "View Summary (Balance, Income, Expenses)",
        "View Monthly Report",
        "View All Transactions",
        "Export to CSV",
        "Generate Expense Chart" if VISUALIZATION_AVAILABLE else "Generate Expense Chart (matplotlib required)",
        "Launch GUI Mode",
        "Exit"
    ]
    print_menu("MAIN MENU", menu_options)


def handle_add_income():
    """
    Handle the add income menu option.
    
    Prompts user for income details and adds the income entry.
    
    Returns:
        None
    """
    print_header("ADD INCOME")
    
    # Get amount with validation
    amount = get_valid_input(
        "Enter income amount: $",
        input_type="float",
        min_value=0.01
    )
    
    if amount is None:
        print("\n❌ Invalid amount. Operation cancelled.")
        return
    
    # Get description
    description = input("Enter description (e.g., Salary, Freelance): ").strip()
    if not description:
        description = "Income"
    
    # Add the income
    success, message = add_income(amount, description)
    
    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")


def handle_add_expense():
    """
    Handle the add expense menu option.
    
    Prompts user for expense details including category and adds the expense entry.
    
    Returns:
        None
    """
    print_header("ADD EXPENSE")
    
    # Display categories
    categories = get_categories()
    print("\nAvailable Categories:")
    for idx, category in enumerate(categories, 1):
        print(f"  {idx}. {category}")
    
    # Get category selection
    category_num = get_valid_input(
        f"\nSelect category (1-{len(categories)}): ",
        input_type="int",
        min_value=1,
        max_value=len(categories)
    )
    
    if category_num is None:
        print("\n❌ Invalid category selection. Operation cancelled.")
        return
    
    category = categories[category_num - 1]
    
    # Get amount with validation
    amount = get_valid_input(
        "Enter expense amount: $",
        input_type="float",
        min_value=0.01
    )
    
    if amount is None:
        print("\n❌ Invalid amount. Operation cancelled.")
        return
    
    # Get description
    description = input("Enter description: ").strip()
    if not description:
        description = f"{category} expense"
    
    # Add the expense
    success, message = add_expense(amount, category, description)
    
    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")


def handle_view_summary():
    """
    Handle the view summary menu option.
    
    Displays total income, total expenses, and current balance.
    
    Returns:
        None
    """
    print_header("FINANCIAL SUMMARY")
    display_summary()


def handle_monthly_report():
    """
    Handle the monthly report menu option.
    
    Prompts user for month and year, then displays filtered report.
    
    Returns:
        None
    """
    print_header("MONTHLY REPORT")
    
    # Get month
    month = get_valid_input(
        "Enter month (1-12): ",
        input_type="int",
        min_value=1,
        max_value=12
    )
    
    if month is None:
        print("\n❌ Invalid month. Operation cancelled.")
        return
    
    # Get year
    from datetime import datetime
    current_year = datetime.now().year
    
    year = get_valid_input(
        f"Enter year (2000-{current_year}): ",
        input_type="int",
        min_value=2000,
        max_value=current_year
    )
    
    if year is None:
        print("\n❌ Invalid year. Operation cancelled.")
        return
    
    display_monthly_report(month, year)


def handle_view_transactions():
    """
    Handle the view all transactions menu option.
    
    Returns:
        None
    """
    print_header("ALL TRANSACTIONS")
    display_all_transactions()


def handle_export_csv():
    """
    Handle the export to CSV menu option.
    
    Exports all transaction data to a CSV file.
    
    Returns:
        None
    """
    print_header("EXPORT TO CSV")
    
    filename = input("Enter filename (default: expenses.csv): ").strip()
    if not filename:
        filename = "expenses.csv"
    
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    success, message = export_to_csv(filename)
    
    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")


def handle_generate_chart():
    """
    Handle the generate expense chart menu option.
    
    Generates a visual bar chart of monthly expenses.
    
    Returns:
        None
    """
    print_header("GENERATE EXPENSE CHART")
    
    if not VISUALIZATION_AVAILABLE:
        print("\n❌ matplotlib is not installed.")
        print("Install it using: pip install matplotlib")
        return
    
    # Get month
    month = get_valid_input(
        "Enter month (1-12) or 0 for all months: ",
        input_type="int",
        min_value=0,
        max_value=12
    )
    
    if month is None:
        print("\n❌ Invalid month. Operation cancelled.")
        return
    
    # Get year
    from datetime import datetime
    current_year = datetime.now().year
    
    year = get_valid_input(
        f"Enter year (2000-{current_year}): ",
        input_type="int",
        min_value=2000,
        max_value=current_year
    )
    
    if year is None:
        print("\n❌ Invalid year. Operation cancelled.")
        return
    
    success, message = generate_expense_chart(month if month > 0 else None, year)
    
    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")


def handle_gui_mode():
    """
    Handle the launch GUI mode menu option.
    
    Attempts to launch the Tkinter GUI version of the application.
    
    Returns:
        None
    """
    print_header("GUI MODE")
    
    try:
        from gui import launch_gui
        print("\nLaunching GUI mode...")
        print("(Close the GUI window to return to console mode)\n")
        launch_gui()
        print("\nReturned to console mode.")
    except ImportError as e:
        print(f"\n❌ Could not launch GUI: {e}")
        print("Make sure tkinter is installed on your system.")
    except Exception as e:
        print(f"\n❌ Error launching GUI: {e}")


def main():
    """
    Main function - Application entry point.
    
    Initializes the application and runs the main menu loop.
    
    Returns:
        None
    """
    # Initialize data file if it doesn't exist
    initialize_data_file()
    
    print("\n" + "=" * 50)
    print("   Welcome to Smart Expense Tracker!")
    print("   Your Personal Finance Management Tool")
    print("=" * 50)
    
    while True:
        print()
        display_main_menu()
        
        choice = get_valid_input(
            "\nEnter your choice (1-9): ",
            input_type="int",
            min_value=1,
            max_value=9
        )
        
        if choice is None:
            print("\n❌ Invalid choice. Please enter a number between 1 and 9.")
            pause()
            continue
        
        if choice == 1:
            handle_add_income()
        elif choice == 2:
            handle_add_expense()
        elif choice == 3:
            handle_view_summary()
        elif choice == 4:
            handle_monthly_report()
        elif choice == 5:
            handle_view_transactions()
        elif choice == 6:
            handle_export_csv()
        elif choice == 7:
            handle_generate_chart()
        elif choice == 8:
            handle_gui_mode()
        elif choice == 9:
            print("\n" + "=" * 50)
            print("   Thank you for using Smart Expense Tracker!")
            print("   Goodbye! 💰")
            print("=" * 50 + "\n")
            sys.exit(0)
        
        pause()


if __name__ == "__main__":
    main()