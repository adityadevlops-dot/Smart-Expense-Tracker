# 💰 Smart Expense Tracker

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A comprehensive, production-ready Python expense tracking application built with **Streamlit**. Track your income and expenses, generate reports, visualize spending patterns, and export data - all in one powerful interactive web app.

---

## ✨ Features

### Core Features
- ➕ **Add Income** - Record your earnings with descriptions
- ➖ **Add Expenses** - Track spending across multiple categories
- 📊 **View Summary** - See total income, expenses, and current balance
- 📅 **Monthly Reports** - Filter and analyze transactions by month/year
- 💾 **Persistent Storage** - All data saved automatically in JSON format
- ✅ **Input Validation** - Robust error handling and data validation
- 🎨 **Interactive Dashboard** - Beautiful Streamlit web interface

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
- 📈 **Data Visualization** - Interactive charts with Plotly/Matplotlib
- 💡 **Smart Analytics** - Category-wise spending breakdown
- 🔄 **Real-time Updates** - Instant balance calculations

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Core programming language |
| Streamlit | Web framework & UI |
| JSON | Data persistence |
| Pandas | Data manipulation |
| Plotly/Matplotlib | Data visualization |
| datetime | Date and time handling |

---

## 📁 Project Structure
```
smart-expense-tracker/
│
├── app.py                 # Main Streamlit application
├── pages/                 # Streamlit multi-page app pages
│   ├── add_expense.py
│   ├── add_income.py
│   ├── view_reports.py
│   └── visualizations.py
├── utils/                 # Utility modules
│   ├── storage.py         # JSON file operations
│   ├── expense.py         # Expense logic
│   └── helpers.py         # Helper functions
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
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The app will open in your default browser at `http://localhost:8501`

---

## 📖 Usage

### Dashboard Features
- **Home Page** - Overview of income, expenses, and balance
- **Add Income** - Add new income entries
- **Add Expense** - Record new expenses with category selection
- **View Reports** - Filter transactions by date/category
- **Visualizations** - Interactive charts and analytics
- **Export Data** - Download transactions as CSV

### Example Workflow
1. Open the app (`streamlit run app.py`)
2. Click "Add Expense" from the sidebar
3. Enter amount, select category, add description
4. Click "Save" - data is stored instantly
5. View your balance and reports in real-time

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
    },
    {
      "id": 2,
      "type": "income",
      "amount": 5000,
      "category": "Salary",
      "description": "Monthly salary",
      "date": "2026-02-01"
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
- Track spending trends

### Interactive Charts & Graphs
- 📊 Pie charts for spending distribution
- 📈 Bar charts for monthly trends
- 📉 Line charts for balance history
- 🎯 Category analysis with drill-down

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Port 8501 is already in use
**Solution:** Run on a different port
```bash
streamlit run app.py --server.port 8502
```

### Issue: `data.json` not found
**Solution:** The file is created automatically on first run. If it doesn't appear, check folder permissions.

### Issue: Changes not reflecting
**Solution:** Streamlit auto-reloads. If not working, restart the app:
```bash
streamlit run app.py --logger.level=debug
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
- GitHub: [https://github.com/adityadevlops-dot](https://github.com/adityadevlops-dot)

---

## 📮 Support

If you have any questions or issues, please open an issue on [GitHub Issues](https://github.com/yourusername/smart-expense-tracker/issues).

---

## 🙏 Acknowledgments

- Thanks to **Streamlit** for the amazing framework
- Python community for excellent libraries
- All users for their feedback and support

---

**Last Updated:** February 5, 2026  
**Version:** 1.0.0