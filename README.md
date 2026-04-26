# Smart Expense Tracker

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-ready Python expense tracking application built with **Streamlit**. Manage income and expenses, generate reports, visualize spending patterns, and export data with ease.

## Overview

Smart Expense Tracker is a comprehensive personal finance management tool designed for users who need quick and efficient expense tracking with visual insights. Built with Python and Streamlit, it provides an intuitive interface for managing transactions across multiple categories.

## Features

### Core Functionality
- Add and manage income entries
- Track expenses across multiple predefined categories
- View real-time account summary (income, expenses, balance)
- Generate monthly reports with date/category filtering
- Automatic persistent storage in JSON format
- Input validation and error handling
- Interactive web-based dashboard

### Data Management
- CSV export for all transactions
- Category-wise spending breakdown
- Monthly transaction filtering
- Real-time balance calculations
- Transaction history with timestamps

### Available Expense Categories
- Food
- Travel
- Rent
- Utilities
- Entertainment
- Healthcare
- Shopping
- Education
- Others

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Framework | Streamlit |
| Data Format | JSON |
| Data Analysis | Pandas |
| Visualization | Plotly/Matplotlib |
| Utilities | datetime module |

## Project Structure

```
smart-expense-tracker/
├── app.py                      # Main Streamlit application
├── pages/                      # Multi-page components
│   ├── add_expense.py         # Expense entry interface
│   ├── add_income.py          # Income entry interface
│   ├── view_reports.py        # Report generation and filtering
│   └── visualizations.py      # Charts and data visualization
├── utils/                      # Utility modules
│   ├── storage.py             # JSON file operations
│   ├── expense.py             # Expense processing logic
│   └── helpers.py             # Helper functions
├── data.json                  # Transaction storage
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # Documentation
```

## Application Flow

```
┌─────────────────────────────────────────┐
│       User Launches Application         │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
    ┌───▼──────┐    ┌─────▼────┐
    │ Dashboard│    │  Sidebar  │
    └───┬──────┘    │ Navigation│
        │           └─────┬────┘
        │                 │
    ┌───┴─────────────────┴──────┐
    │                             │
┌───▼────┐  ┌────────┐  ┌──────┐ │
│Add     │  │Add     │  │View  │ │
│Expense │  │Income  │  │Report│ │
└───┬────┘  └────┬───┘  └──┬───┘ │
    │            │         │     │
    └────────────┼─────────┘     │
                 ▼                │
    ┌──────────────────────┐     │
    │  Validate & Process  │     │
    │      Input Data      │     │
    └──────┬───────────────┘     │
           │                      │
        ┌──▼──────────┐           │
        │  Save to    │           │
        │  data.json  │           │
        └──┬──────────┘           │
           │                      │
        ┌──▼──────────────────────┼──┐
        │  Display Results &      │  │
        │  Generate Visualizations│  │
        └───────────────────────┬─┘  │
                                 │   │
                    ┌────────────┴───┘
                    │
            ┌───────▼────────┐
            │ User Dashboard │
            │ with Charts    │
            └────────────────┘
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/adityadevlops-dot/Smart-Expense-Tracker.git
   cd Smart-Expense-Tracker
   ```

2. **Create virtual environment** (recommended)
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
   
   The app will open automatically at `http://localhost:8501`

## Usage

### Getting Started

1. Launch the application with `streamlit run app.py`
2. Navigate using the sidebar menu
3. Select your desired action:
   - **Add Expense**: Record new spending
   - **Add Income**: Log earnings
   - **View Reports**: Analyze transactions
   - **Visualizations**: View charts and trends

### Workflow Example

```
1. Launch App
   ↓
2. Navigate to "Add Expense"
   ↓
3. Enter Amount → Select Category → Add Description
   ↓
4. Click "Save"
   ↓
5. View updated balance in Dashboard
   ↓
6. Generate reports for analysis
```

### Data Format

Transactions are stored in `data.json` with the following structure:

```json
{
  "transactions": [
    {
      "id": 1,
      "type": "expense",
      "amount": 500,
      "category": "Food",
      "description": "Grocery shopping",
      "date": "2026-04-26"
    },
    {
      "id": 2,
      "type": "income",
      "amount": 5000,
      "category": "Salary",
      "description": "Monthly salary",
      "date": "2026-04-01"
    }
  ]
}
```

## Reports & Visualization

### Report Features
- Monthly transaction summaries
- Category-wise expense breakdown
- Income vs expense comparison
- Spending trend analysis
- Custom date range filtering

### Available Charts
- Pie charts for spending distribution
- Bar charts for monthly trends
- Line charts for balance progression
- Category drill-down analysis

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: streamlit` | Run `pip install -r requirements.txt` |
| Port 8501 already in use | Use `streamlit run app.py --server.port 8502` |
| `data.json` not found | App creates it automatically on first run |
| App not reflecting changes | Restart with `streamlit run app.py --logger.level=debug` |

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## License

Licensed under MIT License - see [LICENSE](LICENSE) for details.

## Author

**Aditya**  
GitHub: [adityadevlops-dot](https://github.com/adityadevlops-dot)

## Support

For issues or questions, open an issue on [GitHub Issues](https://github.com/adityadevlops-dot/Smart-Expense-Tracker/issues).

---

**Last Updated:** April 2026  
**Version:** 1.0.0
