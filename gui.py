#!/usr/bin/env python3
"""
GUI Module - Tkinter-based graphical user interface for the expense tracker.

This module provides an optional GUI interface for users who prefer
graphical interaction over the console interface.

Author: [Your Name]
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Optional

from expense import add_income, add_expense, get_categories
from storage import load_data, initialize_data_file
from report import format_currency, MONTH_NAMES
from utils import export_to_csv


class ExpenseTrackerGUI:
    """
    Main GUI class for the Smart Expense Tracker application.
    
    Provides a graphical interface for all expense tracking operations.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI application.
        
        Args:
            root: The Tkinter root window.
        """
        self.root = root
        self.root.title("Smart Expense Tracker")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#28A745',
            'danger': '#DC3545',
            'warning': '#FFC107',
            'light': '#F8F9FA',
            'dark': '#343A40'
        }
        
        # Initialize data
        initialize_data_file()
        
        # Create main container
        self.create_widgets()
        
        # Load initial data
        self.refresh_data()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Summary section
        self.create_summary_section(main_frame)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tabs
        self.create_add_transaction_tab()
        self.create_transactions_tab()
        self.create_reports_tab()
    
    def create_header(self, parent):
        """Create the header section."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(
            header_frame,
            text="💰 Smart Expense Tracker",
            font=('Helvetica', 24, 'bold')
        )
        title_label.pack(side=tk.LEFT)
        
        # Refresh button
        refresh_btn = ttk.Button(
            header_frame,
            text="🔄 Refresh",
            command=self.refresh_data
        )
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Export button
        export_btn = ttk.Button(
            header_frame,
            text="📁 Export CSV",
            command=self.export_csv
        )
        export_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_summary_section(self, parent):
        """Create the summary cards section."""
        summary_frame = ttk.Frame(parent)
        summary_frame.pack(fill=tk.X, pady=10)
        
        # Configure grid columns
        summary_frame.columnconfigure(0, weight=1)
        summary_frame.columnconfigure(1, weight=1)
        summary_frame.columnconfigure(2, weight=1)
        
        # Income card
        income_card = ttk.LabelFrame(summary_frame, text="💵 Total Income", padding=10)
        income_card.grid(row=0, column=0, padx=5, sticky="nsew")
        
        self.income_label = ttk.Label(
            income_card,
            text="$0.00",
            font=('Helvetica', 20, 'bold'),
            foreground='green'
        )
        self.income_label.pack()
        
        # Expense card
        expense_card = ttk.LabelFrame(summary_frame, text="💸 Total Expenses", padding=10)
        expense_card.grid(row=0, column=1, padx=5, sticky="nsew")
        
        self.expense_label = ttk.Label(
            expense_card,
            text="$0.00",
            font=('Helvetica', 20, 'bold'),
            foreground='red'
        )
        self.expense_label.pack()
        
        # Balance card
        balance_card = ttk.LabelFrame(summary_frame, text="📊 Current Balance", padding=10)
        balance_card.grid(row=0, column=2, padx=5, sticky="nsew")
        
        self.balance_label = ttk.Label(
            balance_card,
            text="$0.00",
            font=('Helvetica', 20, 'bold'),
            foreground='blue'
        )
        self.balance_label.pack()
    
    def create_add_transaction_tab(self):
        """Create the Add Transaction tab."""
        add_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(add_frame, text="➕ Add Transaction")
        
        # Transaction type selection
        type_frame = ttk.LabelFrame(add_frame, text="Transaction Type", padding=10)
        type_frame.pack(fill=tk.X, pady=10)
        
        self.transaction_type = tk.StringVar(value="expense")
        
        ttk.Radiobutton(
            type_frame,
            text="💸 Expense",
            variable=self.transaction_type,
            value="expense",
            command=self.toggle_category
        ).pack(side=tk.LEFT, padx=20)
        
        ttk.Radiobutton(
            type_frame,
            text="💵 Income",
            variable=self.transaction_type,
            value="income",
            command=self.toggle_category
        ).pack(side=tk.LEFT, padx=20)
        
        # Input fields
        fields_frame = ttk.Frame(add_frame)
        fields_frame.pack(fill=tk.X, pady=10)
        
        # Amount
        ttk.Label(fields_frame, text="Amount ($):", font=('Helvetica', 12)).pack(anchor=tk.W)
        self.amount_entry = ttk.Entry(fields_frame, font=('Helvetica', 14))
        self.amount_entry.pack(fill=tk.X, pady=5)
        
        # Category (for expenses)
        self.category_label = ttk.Label(fields_frame, text="Category:", font=('Helvetica', 12))
        self.category_label.pack(anchor=tk.W, pady=(10, 0))
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.category_var,
            values=get_categories(),
            font=('Helvetica', 12),
            state='readonly'
        )
        self.category_combo.pack(fill=tk.X, pady=5)
        self.category_combo.current(0)
        
        # Description
        ttk.Label(fields_frame, text="Description:", font=('Helvetica', 12)).pack(anchor=tk.W, pady=(10, 0))
        self.description_entry = ttk.Entry(fields_frame, font=('Helvetica', 12))
        self.description_entry.pack(fill=tk.X, pady=5)
        
        # Submit button
        submit_btn = ttk.Button(
            add_frame,
            text="✅ Add Transaction",
            command=self.add_transaction,
            style='Accent.TButton'
        )
        submit_btn.pack(pady=20)
        
        # Status label
        self.status_label = ttk.Label(add_frame, text="", font=('Helvetica', 11))
        self.status_label.pack()
    
    def create_transactions_tab(self):
        """Create the Transactions list tab."""
        trans_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(trans_frame, text="📋 Transactions")
        
        # Create treeview with scrollbar
        tree_frame = ttk.Frame(trans_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ('ID', 'Date', 'Type', 'Category', 'Amount', 'Description')
        self.transactions_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        # Configure columns
        self.transactions_tree.heading('ID', text='ID')
        self.transactions_tree.heading('Date', text='Date')
        self.transactions_tree.heading('Type', text='Type')
        self.transactions_tree.heading('Category', text='Category')
        self.transactions_tree.heading('Amount', text='Amount')
        self.transactions_tree.heading('Description', text='Description')
        
        self.transactions_tree.column('ID', width=50)
        self.transactions_tree.column('Date', width=100)
        self.transactions_tree.column('Type', width=80)
        self.transactions_tree.column('Category', width=100)
        self.transactions_tree.column('Amount', width=100)
        self.transactions_tree.column('Description', width=200)
        
        self.transactions_tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.transactions_tree.yview)
        
        # Configure row tags for colors
        self.transactions_tree.tag_configure('income', background='#d4edda')
        self.transactions_tree.tag_configure('expense', background='#f8d7da')
    
    def create_reports_tab(self):
        """Create the Reports tab."""
        reports_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Month/Year selection
        filter_frame = ttk.LabelFrame(reports_frame, text="Filter", padding=10)
        filter_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(filter_frame, text="Month:").pack(side=tk.LEFT, padx=5)
        
        self.month_var = tk.StringVar()
        month_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.month_var,
            values=['All'] + MONTH_NAMES,
            width=15,
            state='readonly'
        )
        month_combo.pack(side=tk.LEFT, padx=5)
        month_combo.current(datetime.now().month)
        
        ttk.Label(filter_frame, text="Year:").pack(side=tk.LEFT, padx=5)
        
        current_year = datetime.now().year
        self.year_var = tk.StringVar(value=str(current_year))
        year_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.year_var,
            values=[str(y) for y in range(2020, current_year + 1)],
            width=10,
            state='readonly'
        )
        year_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            filter_frame,
            text="Generate Report",
            command=self.generate_report
        ).pack(side=tk.LEFT, padx=20)
        
        # Report display area
        self.report_text = tk.Text(
            reports_frame,
            height=20,
            font=('Courier', 11),
            wrap=tk.WORD
        )
        self.report_text.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def toggle_category(self):
        """Toggle category field visibility based on transaction type."""
        if self.transaction_type.get() == "income":
            self.category_label.pack_forget()
            self.category_combo.pack_forget()
        else:
            self.category_label.pack(anchor=tk.W, pady=(10, 0))
            self.category_combo.pack(fill=tk.X, pady=5)
    
    def add_transaction(self):
        """Handle adding a new transaction."""
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount")
            return
        
        description = self.description_entry.get().strip() or "Transaction"
        
        if self.transaction_type.get() == "income":
            success, message = add_income(amount, description)
        else:
            category = self.category_var.get()
            success, message = add_expense(amount, category, description)
        
        if success:
            self.status_label.config(text=f"✅ {message}", foreground='green')
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.refresh_data()
        else:
            self.status_label.config(text=f"❌ {message}", foreground='red')
    
    def refresh_data(self):
        """Refresh all displayed data."""
        data = load_data()
        
        # Update summary cards
        self.income_label.config(text=format_currency(data.get("total_income", 0)))
        self.expense_label.config(text=format_currency(data.get("total_expense", 0)))
        
        balance = data.get("balance", 0)
        color = 'green' if balance >= 0 else 'red'
        self.balance_label.config(text=format_currency(balance), foreground=color)
        
        # Update transactions tree
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
        
        transactions = sorted(
            data.get("transactions", []),
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )
        
        for t in transactions:
            tag = t.get("type", "expense")
            self.transactions_tree.insert(
                '',
                'end',
                values=(
                    t.get("id", ""),
                    t.get("date", ""),
                    t.get("type", "").capitalize(),
                    t.get("category", ""),
                    format_currency(t.get("amount", 0)),
                    t.get("description", "")[:30]
                ),
                tags=(tag,)
            )
    
    def generate_report(self):
        """Generate a monthly report."""
        self.report_text.delete(1.0, tk.END)
        
        data = load_data()
        year = int(self.year_var.get())
        month_str = self.month_var.get()
        
        if month_str == 'All':
            transactions = [t for t in data["transactions"] if t.get("year") == year]
            period = f"Year {year}"
        else:
            month = MONTH_NAMES.index(month_str) + 1
            transactions = [
                t for t in data["transactions"]
                if t.get("month") == month and t.get("year") == year
            ]
            period = f"{month_str} {year}"
        
        # Generate report text
        report = f"{'=' * 50}\n"
        report += f"FINANCIAL REPORT - {period}\n"
        report += f"{'=' * 50}\n\n"
        
        if not transactions:
            report += "No transactions found for this period.\n"
        else:
            income = sum(t["amount"] for t in transactions if t["type"] == "income")
            expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
            net = income - expense
            
            report += f"📊 SUMMARY\n"
            report += f"{'-' * 40}\n"
            report += f"Total Income:    {format_currency(income):>15}\n"
            report += f"Total Expenses:  {format_currency(expense):>15}\n"
            report += f"Net Balance:     {format_currency(net):>15}\n\n"
            
            # Category breakdown - only if there are expenses
            if expense > 0:
                report += f"📈 EXPENSE BY CATEGORY\n"
                report += f"{'-' * 40}\n"
                
                category_totals = {}
                for t in transactions:
                    if t["type"] == "expense":
                        cat = t.get("category", "Others")
                        category_totals[cat] = category_totals.get(cat, 0) + t["amount"]
                
                for cat, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
                    pct = (amount / expense * 100) if expense > 0 else 0
                    report += f"{cat:<15} {format_currency(amount):>12} ({pct:5.1f}%)\n"
            else:
                report += f"No expenses for this period.\n"
            
            report += f"\n📝 TRANSACTION COUNT: {len(transactions)}\n"
        
        self.report_text.insert(tk.END, report)
    
    def export_csv(self):
        """Export data to CSV file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="expenses.csv"
        )
        
        if filename:
            success, message = export_to_csv(filename)
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)


def launch_gui():
    """
    Launch the GUI application.
    
    This function initializes and runs the Tkinter main loop.
    
    Returns:
        None
    """
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()