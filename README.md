# 💰 Smart Expense Tracker

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A comprehensive, production-ready Python expense tracking application with both console and GUI interfaces. Track your income and expenses, generate reports, visualize spending patterns, and export data - all in one powerful tool.

![Smart Expense Tracker](https://via.placeholder.com/800x400/2E86AB/FFFFFF?text=Smart+Expense+Tracker)

---

## ✨ Features

### Core Features
- ➕ **Add Income** - Record your earnings with descriptions
- ➖ **Add Expenses** - Track spending across multiple categories
- 📊 **View Summary** - See total income, expenses, and current balance
- 📅 **Monthly Reports** - Filter and analyze transactions by month/year
- 💾 **Persistent Storage** - All data saved automatically in JSON format
- ✅ **Input Validation** - Robust error handling and data validation
- 🎯 **User-Friendly Menu** - Intuitive console-based navigation

### Expense Categories
- 🍔 Food
- ✈️ Travel
- 🏠 Rent
- ⚡ Utilities
- 🎬 Entertainment
- 🏥 Healthcare
- 🛒 Shopping
- 📚 Education
- 📦 Others

### Optional Enhancements
- 📁 **CSV Export** - Export all transactions to spreadsheet-compatible format
- 📈 **Data Visualization** - Generate beautiful charts with matplotlib
- 🖥️ **GUI Mode** - Optional Tkinter graphical interface
- 📊 **Category Analysis** - Visual breakdown of spending by category

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Core programming language |
| JSON | Data persistence |
| datetime | Date and time handling |
| csv | CSV export functionality |
| matplotlib | Data visualization (optional) |
| Tkinter | GUI interface (optional) |

---

## 📁 Project Structure
```
smart-expense-tracker/
│
├── main.py # Application entry point & menu system
├── expense.py # Income and expense management logic
├── storage.py # JSON file operations for data persistence
├── report.py # Report generation and formatting
├── utils.py # Helper functions and utilities
├── visualization.py # Chart generation with matplotlib
├── gui.py # Optional Tkinter GUI interface
├── data.json # Persistent data storage file
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smart-expense-tracker.git
   cd smart-expense-tracker

2. Create a virtual environment (recommended)

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. install dependencies
# Core functionality (no external dependencies)
# For visualization features:
pip install -r requirements.txt

4. Run the application
python main.py
