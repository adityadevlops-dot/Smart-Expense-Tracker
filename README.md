# 💰 Smart Expense Tracker

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A comprehensive, production-ready Python expense tracking application with both console and GUI interfaces. Track your income and expenses, generate reports, visualize spending patterns, and export data - all in one powerful tool.


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
├── main.py                # Application entry point & menu system
├── expense.py             # Income and expense management logic
├── storage.py             # JSON file operations for data persistence
├── report.py              # Report generation and formatting
├── utils.py               # Helper functions and utilities
├── visualization.py       # Chart generation with matplotlib
├── gui.py                 # Optional Tkinter GUI interface
├── data.json              # Persistent data storage file
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smart-expense-tracker.git
   cd smart-expense-tracker
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Core functionality (no external dependencies required)
   # For visualization features, install:
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

---

## 📖 Usage

### Console Menu
```
===============================================
      💰 SMART EXPENSE TRACKER 💰
===============================================
1. Add Income
2. Add Expense
3. View Summary
4. View Monthly Report
5. Export to CSV
6. View Visualizations
7. Exit
===============================================
```

### Example: Adding an Expense
```
Enter amount: 500
Select category:
1. Food
2. Travel
3. Rent
4. Utilities
5. Entertainment
6. Healthcare
7. Shopping
8. Education
9. Others

Enter description: Grocery shopping
```

---

## 💾 Data Storage

Your transactions are automatically saved in `data.json` with the following structure:

```json
{
  "transactions": [
    {
      "id": 1,
      "type": "expense",
      "amount": 500,
      "category": "Food",
      "description": "Grocery shopping",
      "date": "2026-02-05"
    }
  ]
}
```

---

## 📊 Reports & Visualization

### Monthly Reports
- View all transactions for a specific month/year
- See category-wise breakdown
- Calculate total income and expenses

### Charts & Graphs
- Pie charts for spending distribution
- Bar charts for monthly trends
- Line charts for balance history

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'matplotlib'`
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: `data.json` not found
**Solution:** The file is created automatically on first run. If it doesn't appear, check folder permissions.

### Issue: GUI not opening
**Solution:** Tkinter should be installed with Python. On Linux, install it separately:
```bash
sudo apt-get install python3-tk
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Aditya**
- GitHub: [https://github.com/adityadevlops-dot)

---

## 📮 Support

If you have any questions or issues, please open an issue on [GitHub Issues](https://github.com/yourusername/smart-expense-tracker/issues).

---

## 🙏 Acknowledgments

- Thanks to the Python community for amazing libraries
- All users for their feedback and support

---

**Last Updated:** February 5, 2026  
**Version:** 1.0.0
