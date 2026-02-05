import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime, date

# ============================================
# CONFIGURATION
# ============================================

DATA_FILE = "data.json"

EXPENSE_CATEGORIES = [
    "Food & Dining",
    "Rent & Housing",
    "Transportation",
    "Shopping",
    "Utilities",
    "Healthcare",
    "Education",
    "Entertainment",
    "Groceries",
    "Other"
]

INCOME_SOURCES = [
    "Salary",
    "Freelance",
    "Investments",
    "Business",
    "Rental Income",
    "Other"
]

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PROFESSIONAL CSS STYLING
# ============================================

st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1400px;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    
    /* App Logo */
    .app-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.5rem 1rem;
        margin-bottom: 1.5rem;
    }
    
    .app-logo-icon {
        width: 32px;
        height: 32px;
        background: #3b82f6;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 14px;
    }
    
    .app-logo-text {
        font-size: 16px;
        font-weight: 600;
        color: #111827;
    }
    
    /* Page Header */
    .page-header {
        margin-bottom: 1.5rem;
    }
    
    .page-title {
        font-size: 24px;
        font-weight: 600;
        color: #111827;
        margin: 0 0 4px 0;
    }
    
    .page-subtitle {
        font-size: 14px;
        color: #6b7280;
        margin: 0;
    }
    
    /* Stat Cards */
    .stats-container {
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
    }
    
    .stat-card {
        flex: 1;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 16px 20px;
    }
    
    .stat-label {
        font-size: 13px;
        font-weight: 500;
        color: #6b7280;
        margin-bottom: 4px;
    }
    
    .stat-value {
        font-size: 24px;
        font-weight: 600;
        color: #111827;
    }
    
    .stat-value.income {
        color: #059669;
    }
    
    .stat-value.expense {
        color: #dc2626;
    }
    
    .stat-value.balance {
        color: #111827;
    }
    
    .stat-change {
        font-size: 12px;
        color: #6b7280;
        margin-top: 4px;
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #111827;
        margin: 0;
    }
    
    .section-link {
        font-size: 13px;
        color: #3b82f6;
        text-decoration: none;
        cursor: pointer;
    }
    
    /* Card Container */
    .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .card-header {
        font-size: 14px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #f3f4f6;
    }
    
    /* Transaction Table */
    .transaction-row {
        display: flex;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .transaction-row:last-child {
        border-bottom: none;
    }
    
    .transaction-icon {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        font-size: 14px;
    }
    
    .transaction-icon.income {
        background: #ecfdf5;
        color: #059669;
    }
    
    .transaction-icon.expense {
        background: #fef2f2;
        color: #dc2626;
    }
    
    .transaction-details {
        flex: 1;
    }
    
    .transaction-title {
        font-size: 14px;
        font-weight: 500;
        color: #111827;
    }
    
    .transaction-meta {
        font-size: 12px;
        color: #6b7280;
    }
    
    .transaction-amount {
        font-size: 14px;
        font-weight: 600;
        text-align: right;
    }
    
    .transaction-amount.income {
        color: #059669;
    }
    
    .transaction-amount.expense {
        color: #dc2626;
    }
    
    /* Category Progress */
    .category-item {
        margin-bottom: 16px;
    }
    
    .category-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
    }
    
    .category-name {
        font-size: 13px;
        font-weight: 500;
        color: #374151;
    }
    
    .category-amount {
        font-size: 13px;
        font-weight: 500;
        color: #111827;
    }
    
    .progress-bar {
        height: 6px;
        background: #f3f4f6;
        border-radius: 3px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: #3b82f6;
        border-radius: 3px;
    }
    
    /* Form Styles */
    .form-container {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 24px;
    }
    
    .form-title {
        font-size: 16px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 20px;
    }
    
    /* Input Overrides */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stDateInput > div > div > input {
        border: 1px solid #d1d5db;
        border-radius: 6px;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
    }
    
    /* Button Styles */
    .stButton > button {
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: 500;
        transition: background 0.2s;
    }
    
    .stButton > button:hover {
        background: #2563eb;
    }
    
    .stButton > button:active {
        background: #1d4ed8;
    }
    
    /* Secondary Button */
    .secondary-btn > button {
        background: #ffffff;
        color: #374151;
        border: 1px solid #d1d5db;
    }
    
    .secondary-btn > button:hover {
        background: #f9fafb;
    }
    
    /* Danger Button */
    .danger-btn > button {
        background: #dc2626;
    }
    
    .danger-btn > button:hover {
        background: #b91c1c;
    }
    
    /* Alert Styles */
    .stSuccess {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
    }
    
    .stError {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #991b1b;
    }
    
    .stWarning {
        background: #fffbeb;
        border: 1px solid #fde68a;
        color: #92400e;
    }
    
    .stInfo {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e40af;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 40px 20px;
        color: #6b7280;
    }
    
    .empty-state-icon {
        font-size: 32px;
        margin-bottom: 12px;
        opacity: 0.5;
    }
    
    .empty-state-text {
        font-size: 14px;
    }
    
    /* Navigation Item */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 12px;
        border-radius: 6px;
        margin-bottom: 4px;
        cursor: pointer;
        transition: background 0.15s;
        font-size: 14px;
        color: #4b5563;
    }
    
    .nav-item:hover {
        background: #f3f4f6;
    }
    
    .nav-item.active {
        background: #eff6ff;
        color: #3b82f6;
    }
    
    .nav-icon {
        width: 18px;
        text-align: center;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 16px;
        font-size: 14px;
    }
    
    /* Metrics Override */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 13px;
        color: #6b7280;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: #e5e7eb;
        margin: 24px 0;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Quick Actions */
    .quick-action {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 14px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        font-size: 13px;
        color: #374151;
        cursor: pointer;
        transition: all 0.15s;
    }
    
    .quick-action:hover {
        background: #f3f4f6;
        border-color: #d1d5db;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# DATA FUNCTIONS
# ============================================

def get_default_data():
    """Return default empty data structure."""
    return {"income": [], "expenses": []}


def load_data():
    """Load data from JSON file."""
    try:
        if not os.path.exists(DATA_FILE):
            save_data(get_default_data())
            return get_default_data()
        
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        
        if "income" not in data:
            data["income"] = []
        if "expenses" not in data:
            data["expenses"] = []
        
        return data
    except Exception:
        return get_default_data()


def save_data(data):
    """Save data to JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception:
        return False


def add_income(amount, source, income_date, description=""):
    """Add new income entry."""
    if amount <= 0:
        return False
    
    data = load_data()
    income_entry = {
        "id": str(uuid.uuid4()),
        "amount": float(amount),
        "source": source,
        "description": description,
        "date": str(income_date),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["income"].append(income_entry)
    return save_data(data)


def add_expense(amount, category, description, expense_date):
    """Add new expense entry."""
    if amount <= 0:
        return False
    
    data = load_data()
    expense_entry = {
        "id": str(uuid.uuid4()),
        "amount": float(amount),
        "category": category,
        "description": description,
        "date": str(expense_date),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["expenses"].append(expense_entry)
    return save_data(data)


def get_total_income(data=None):
    """Calculate total income."""
    if data is None:
        data = load_data()
    return sum(float(entry["amount"]) for entry in data["income"])


def get_total_expenses(data=None):
    """Calculate total expenses."""
    if data is None:
        data = load_data()
    return sum(float(entry["amount"]) for entry in data["expenses"])


def get_balance(data=None):
    """Calculate current balance."""
    if data is None:
        data = load_data()
    return get_total_income(data) - get_total_expenses(data)


def clear_all_data():
    """Clear all data."""
    return save_data(get_default_data())


def get_category_expenses(data=None):
    """Get expenses grouped by category."""
    if data is None:
        data = load_data()
    
    if not data["expenses"]:
        return {}
    
    category_totals = {}
    for entry in data["expenses"]:
        cat = entry["category"]
        amount = float(entry["amount"])
        category_totals[cat] = category_totals.get(cat, 0) + amount
    
    # Sort by amount descending
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_cats)


def get_monthly_data(data=None):
    """Get monthly income and expenses."""
    if data is None:
        data = load_data()
    
    monthly = {}
    
    for entry in data["income"]:
        month = str(entry["date"])[:7]
        if month not in monthly:
            monthly[month] = {"income": 0, "expenses": 0}
        monthly[month]["income"] += float(entry["amount"])
    
    for entry in data["expenses"]:
        month = str(entry["date"])[:7]
        if month not in monthly:
            monthly[month] = {"income": 0, "expenses": 0}
        monthly[month]["expenses"] += float(entry["amount"])
    
    return monthly


def get_recent_transactions(data=None, limit=10):
    """Get recent transactions."""
    if data is None:
        data = load_data()
    
    transactions = []
    
    for entry in data["income"]:
        transactions.append({
            "date": str(entry["date"]),
            "type": "income",
            "category": entry["source"],
            "description": entry.get("description", ""),
            "amount": float(entry["amount"])
        })
    
    for entry in data["expenses"]:
        transactions.append({
            "date": str(entry["date"]),
            "type": "expense",
            "category": entry["category"],
            "description": entry["description"],
            "amount": float(entry["amount"])
        })
    
    # Sort by date descending
    transactions.sort(key=lambda x: x["date"], reverse=True)
    return transactions[:limit]


def export_to_csv(data=None):
    """Export data to CSV."""
    if data is None:
        data = load_data()
    
    records = []
    
    for entry in data["income"]:
        records.append({
            "Date": entry["date"],
            "Type": "Income",
            "Category": entry["source"],
            "Description": entry.get("description", ""),
            "Amount": float(entry["amount"])
        })
    
    for entry in data["expenses"]:
        records.append({
            "Date": entry["date"],
            "Type": "Expense",
            "Category": entry["category"],
            "Description": entry["description"],
            "Amount": -float(entry["amount"])
        })
    
    if not records:
        return "Date,Type,Category,Description,Amount\n"
    
    df = pd.DataFrame(records)
    return df.to_csv(index=False)


def format_currency(amount):
    """Format amount as currency."""
    return f"${amount:,.2f}"


def format_date(date_str):
    """Format date for display."""
    try:
        dt = datetime.strptime(str(date_str), "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except Exception:
        return date_str


# ============================================
# SIDEBAR
# ============================================

def render_sidebar():
    """Render sidebar navigation."""
    with st.sidebar:
        # App Logo - Using HTML/CSS instead of image
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <h1 style="font-size: 3rem; margin: 0;">💳</h1>
            <h2 style="margin: 0.5rem 0 0 0; font-size: 1.3rem;">Smart Expense</h2>
            <p style="margin: 0; font-size: 0.9rem; color: #888;">Tracker</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("#### Menu")
        
        page = st.radio(
            "Navigation",
            options=[
                "Dashboard",
                "Add Income",
                "Add Expense",
                "Reports",
                "Settings"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick Stats
        data = load_data()
        balance = get_balance(data)
        
        st.markdown("#### Account Balance")
        balance_color = "#059669" if balance >= 0 else "#dc2626"
        st.markdown(f"""
            <div style="font-size: 24px; font-weight: 600; color: {balance_color};">
                {format_currency(balance)}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Add Buttons
        st.markdown("#### Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("+ Income", use_container_width=True, key="quick_income"):
                st.session_state.page = "Add Income"
                st.rerun()
        with col2:
            if st.button("+ Expense", use_container_width=True, key="quick_expense"):
                st.session_state.page = "Add Expense"
                st.rerun()
        
        st.markdown("---")
        st.caption("Smart Expense Tracker v1.0")
        
        return page


# ============================================
# DASHBOARD PAGE
# ============================================

def page_dashboard():
    """Render dashboard page."""
    
    # Page Header
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Dashboard</h1>
            <p class="page-subtitle">Overview of your finances</p>
        </div>
    """, unsafe_allow_html=True)
    
    data = load_data()
    
    total_income = get_total_income(data)
    total_expenses = get_total_expenses(data)
    balance = get_balance(data)
    
    # Stats Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Income</div>
                <div class="stat-value income">{format_currency(total_income)}</div>
                <div class="stat-change">{len(data['income'])} transactions</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Expenses</div>
                <div class="stat-value expense">{format_currency(total_expenses)}</div>
                <div class="stat-change">{len(data['expenses'])} transactions</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        balance_class = "income" if balance >= 0 else "expense"
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Current Balance</div>
                <div class="stat-value {balance_class}">{format_currency(balance)}</div>
                <div class="stat-change">Updated just now</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)
    
    # Main Content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Recent Transactions
        st.markdown("""
            <div class="section-header">
                <h3 class="section-title">Recent Transactions</h3>
            </div>
        """, unsafe_allow_html=True)
        
        transactions = get_recent_transactions(data, limit=8)
        
        if transactions:
            st.markdown('<div class="card" style="padding: 12px 16px;">', unsafe_allow_html=True)
            
            for txn in transactions:
                icon_class = "income" if txn["type"] == "income" else "expense"
                icon = "↓" if txn["type"] == "income" else "↑"
                amount_prefix = "+" if txn["type"] == "income" else "-"
                
                st.markdown(f"""
                    <div class="transaction-row">
                        <div class="transaction-icon {icon_class}">{icon}</div>
                        <div class="transaction-details">
                            <div class="transaction-title">{txn['description'] or txn['category']}</div>
                            <div class="transaction-meta">{txn['category']} · {format_date(txn['date'])}</div>
                        </div>
                        <div class="transaction-amount {icon_class}">{amount_prefix}{format_currency(txn['amount'])}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="card">
                    <div class="empty-state">
                        <div class="empty-state-icon">📊</div>
                        <div class="empty-state-text">No transactions yet. Add your first income or expense to get started.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Top Categories
        st.markdown("""
            <div class="section-header">
                <h3 class="section-title">Top Expense Categories</h3>
            </div>
        """, unsafe_allow_html=True)
        
        categories = get_category_expenses(data)
        
        if categories:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            total = sum(categories.values())
            
            for cat, amount in list(categories.items())[:5]:
                pct = (amount / total * 100) if total > 0 else 0
                
                st.markdown(f"""
                    <div class="category-item">
                        <div class="category-header">
                            <span class="category-name">{cat}</span>
                            <span class="category-amount">{format_currency(amount)}</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {pct}%"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="card">
                    <div class="empty-state">
                        <div class="empty-state-icon">📁</div>
                        <div class="empty-state-text">No expense data yet</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Monthly Summary
        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div class="section-header">
                <h3 class="section-title">This Month</h3>
            </div>
        """, unsafe_allow_html=True)
        
        current_month = datetime.now().strftime("%Y-%m")
        monthly_data = get_monthly_data(data)
        
        if current_month in monthly_data:
            month_info = monthly_data[current_month]
            month_income = month_info["income"]
            month_expense = month_info["expenses"]
            month_net = month_income - month_expense
            
            st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                        <span style="color: #6b7280; font-size: 13px;">Income</span>
                        <span style="color: #059669; font-weight: 500;">{format_currency(month_income)}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                        <span style="color: #6b7280; font-size: 13px;">Expenses</span>
                        <span style="color: #dc2626; font-weight: 500;">{format_currency(month_expense)}</span>
                    </div>
                    <div style="border-top: 1px solid #e5e7eb; padding-top: 12px; display: flex; justify-content: space-between;">
                        <span style="font-weight: 500; font-size: 13px;">Net</span>
                        <span style="font-weight: 600; color: {'#059669' if month_net >= 0 else '#dc2626'};">{format_currency(month_net)}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="card">
                    <div style="text-align: center; color: #6b7280; font-size: 13px; padding: 12px 0;">
                        No data for this month
                    </div>
                </div>
            """, unsafe_allow_html=True)


# ============================================
# ADD INCOME PAGE
# ============================================

def page_add_income():
    """Render add income page."""
    
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Add Income</h1>
            <p class="page-subtitle">Record a new income transaction</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("income_form", clear_on_submit=True):
            amount = st.number_input(
                "Amount",
                min_value=0.01,
                value=0.01,
                step=0.01,
                format="%.2f",
                help="Enter the income amount"
            )
            
            source = st.selectbox(
                "Source",
                options=INCOME_SOURCES,
                help="Select the source of income"
            )
            
            description = st.text_input(
                "Description (optional)",
                placeholder="e.g., Monthly salary, Client payment",
                help="Add a brief description"
            )
            
            income_date = st.date_input(
                "Date",
                value=date.today(),
                help="Date of the income"
            )
            
            st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Add Income", use_container_width=True)
            
            if submitted:
                if amount <= 0:
                    st.error("Amount must be greater than 0")
                else:
                    if add_income(amount, source, income_date, description):
                        st.success(f"Successfully added income of {format_currency(amount)}")
                    else:
                        st.error("Failed to save income. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card">
                <div class="card-header">Quick Tips</div>
                <ul style="color: #6b7280; font-size: 13px; padding-left: 20px; margin: 0;">
                    <li style="margin-bottom: 8px;">Record income on the day you receive it</li>
                    <li style="margin-bottom: 8px;">Use clear descriptions for easy tracking</li>
                    <li style="margin-bottom: 8px;">Include all sources of income</li>
                    <li>Regular tracking helps with budgeting</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # Recent Income
        data = load_data()
        recent_income = sorted(data["income"], key=lambda x: x["date"], reverse=True)[:3]
        
        if recent_income:
            st.markdown("""
                <div class="card">
                    <div class="card-header">Recent Income</div>
            """, unsafe_allow_html=True)
            
            for entry in recent_income:
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px;">
                        <span style="color: #6b7280;">{entry['source']}</span>
                        <span style="color: #059669; font-weight: 500;">{format_currency(float(entry['amount']))}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# ADD EXPENSE PAGE
# ============================================

def page_add_expense():
    """Render add expense page."""
    
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Add Expense</h1>
            <p class="page-subtitle">Record a new expense transaction</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("expense_form", clear_on_submit=True):
            amount = st.number_input(
                "Amount",
                min_value=0.01,
                value=0.01,
                step=0.01,
                format="%.2f",
                help="Enter the expense amount"
            )
            
            category = st.selectbox(
                "Category",
                options=EXPENSE_CATEGORIES,
                help="Select expense category"
            )
            
            description = st.text_input(
                "Description",
                placeholder="e.g., Lunch at restaurant, Uber ride",
                help="Brief description of the expense"
            )
            
            expense_date = st.date_input(
                "Date",
                value=date.today(),
                help="Date of the expense"
            )
            
            st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Add Expense", use_container_width=True)
            
            if submitted:
                errors = []
                if amount <= 0:
                    errors.append("Amount must be greater than 0")
                if not description.strip():
                    errors.append("Description is required")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    if add_expense(amount, category, description.strip(), expense_date):
                        st.success(f"Successfully added expense of {format_currency(amount)}")
                    else:
                        st.error("Failed to save expense. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card">
                <div class="card-header">Quick Tips</div>
                <ul style="color: #6b7280; font-size: 13px; padding-left: 20px; margin: 0;">
                    <li style="margin-bottom: 8px;">Record expenses right after purchase</li>
                    <li style="margin-bottom: 8px;">Choose accurate categories</li>
                    <li style="margin-bottom: 8px;">Be specific in descriptions</li>
                    <li>Small expenses add up over time</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # Category breakdown
        categories = get_category_expenses(load_data())
        
        if categories:
            st.markdown("""
                <div class="card">
                    <div class="card-header">Spending by Category</div>
            """, unsafe_allow_html=True)
            
            for cat, amount in list(categories.items())[:4]:
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px;">
                        <span style="color: #6b7280;">{cat}</span>
                        <span style="color: #dc2626; font-weight: 500;">{format_currency(amount)}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# REPORTS PAGE
# ============================================

def page_reports():
    """Render reports page."""
    
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Reports</h1>
            <p class="page-subtitle">Analyze your spending patterns</p>
        </div>
    """, unsafe_allow_html=True)
    
    data = load_data()
    
    if not data["income"] and not data["expenses"]:
        st.info("No data available. Start by adding some income or expenses.")
        return
    
    # Summary Row
    col1, col2, col3, col4 = st.columns(4)
    
    total_income = get_total_income(data)
    total_expenses = get_total_expenses(data)
    balance = get_balance(data)
    total_txns = len(data["income"]) + len(data["expenses"])
    
    with col1:
        st.metric("Total Income", format_currency(total_income))
    with col2:
        st.metric("Total Expenses", format_currency(total_expenses))
    with col3:
        st.metric("Net Balance", format_currency(balance))
    with col4:
        st.metric("Total Transactions", total_txns)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Monthly Overview")
        
        monthly_data = get_monthly_data(data)
        
        if monthly_data:
            months = sorted(monthly_data.keys())
            
            chart_data = pd.DataFrame({
                "Month": months,
                "Income": [monthly_data[m]["income"] for m in months],
                "Expenses": [monthly_data[m]["expenses"] for m in months]
            })
            
            chart_data = chart_data.set_index("Month")
            st.bar_chart(chart_data, color=["#059669", "#dc2626"])
        else:
            st.info("No monthly data available")
    
    with col2:
        st.markdown("#### Expenses by Category")
        
        categories = get_category_expenses(data)
        
        if categories:
            cat_df = pd.DataFrame({
                "Category": list(categories.keys()),
                "Amount": list(categories.values())
            })
            cat_df = cat_df.set_index("Category")
            st.bar_chart(cat_df, color="#3b82f6")
        else:
            st.info("No expense data available")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Detailed Tables
    st.markdown("#### Transaction History")
    
    tab1, tab2, tab3 = st.tabs(["All Transactions", "Income", "Expenses"])
    
    with tab1:
        all_txns = get_recent_transactions(data, limit=50)
        if all_txns:
            df = pd.DataFrame(all_txns)
            df["amount_display"] = df.apply(
                lambda x: f"+{format_currency(x['amount'])}" if x['type'] == 'income' else f"-{format_currency(x['amount'])}",
                axis=1
            )
            df["date"] = df["date"].apply(format_date)
            
            st.dataframe(
                df[["date", "type", "category", "description", "amount_display"]].rename(columns={
                    "date": "Date",
                    "type": "Type",
                    "category": "Category",
                    "description": "Description",
                    "amount_display": "Amount"
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No transactions found")
    
    with tab2:
        if data["income"]:
            income_df = pd.DataFrame(data["income"])
            income_df["date"] = income_df["date"].apply(format_date)
            income_df["amount"] = income_df["amount"].apply(lambda x: format_currency(float(x)))
            
            st.dataframe(
                income_df[["date", "source", "description", "amount"]].rename(columns={
                    "date": "Date",
                    "source": "Source",
                    "description": "Description",
                    "amount": "Amount"
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No income records found")
    
    with tab3:
        if data["expenses"]:
            expense_df = pd.DataFrame(data["expenses"])
            expense_df["date"] = expense_df["date"].apply(format_date)
            expense_df["amount"] = expense_df["amount"].apply(lambda x: format_currency(float(x)))
            
            st.dataframe(
                expense_df[["date", "category", "description", "amount"]].rename(columns={
                    "date": "Date",
                    "category": "Category",
                    "description": "Description",
                    "amount": "Amount"
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No expense records found")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Export
    st.markdown("#### Export Data")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        csv = export_to_csv(data)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"expense_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================
# SETTINGS PAGE
# ============================================

def page_settings():
    """Render settings page."""
    
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Settings</h1>
            <p class="page-subtitle">Manage your data and preferences</p>
        </div>
    """, unsafe_allow_html=True)
    
    data = load_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Data Summary
        st.markdown("""
            <div class="card">
                <div class="card-header">Data Summary</div>
        """, unsafe_allow_html=True)
        
        total_txns = len(data["income"]) + len(data["expenses"])
        
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                <span style="color: #6b7280; font-size: 14px;">Total Transactions</span>
                <span style="font-weight: 500;">{total_txns}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                <span style="color: #6b7280; font-size: 14px;">Income Entries</span>
                <span style="font-weight: 500;">{len(data['income'])}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                <span style="color: #6b7280; font-size: 14px;">Expense Entries</span>
                <span style="font-weight: 500;">{len(data['expenses'])}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #6b7280; font-size: 14px;">Data File</span>
                <span style="font-weight: 500;">{DATA_FILE}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export Section
        st.markdown("""
            <div class="card">
                <div class="card-header">Export Data</div>
        """, unsafe_allow_html=True)
        
        csv = export_to_csv(data)
        st.download_button(
            label="Download CSV Report",
            data=csv,
            file_name=f"expense_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
        
        json_str = json.dumps(data, indent=2, default=str)
        st.download_button(
            label="Download JSON Backup",
            data=json_str,
            file_name=f"backup_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Danger Zone
        st.markdown("""
            <div class="card" style="border-color: #fecaca;">
                <div class="card-header" style="color: #dc2626;">Danger Zone</div>
                <p style="color: #6b7280; font-size: 13px; margin-bottom: 16px;">
                    This action will permanently delete all your data. This cannot be undone.
                </p>
        """, unsafe_allow_html=True)
        
        if "confirm_delete" not in st.session_state:
            st.session_state.confirm_delete = False
        
        if not st.session_state.confirm_delete:
            if st.button("Delete All Data", use_container_width=True, type="secondary"):
                st.session_state.confirm_delete = True
                st.rerun()
        else:
            st.warning("Are you sure? This will delete all your data permanently.")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Yes, Delete", use_container_width=True, type="primary"):
                    if clear_all_data():
                        st.success("All data has been deleted")
                        st.session_state.confirm_delete = False
                        st.rerun()
            with col_b:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.confirm_delete = False
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # About
        st.markdown("""
            <div class="card">
                <div class="card-header">About</div>
                <p style="color: #6b7280; font-size: 13px; margin-bottom: 8px;">
                    <strong>Smart Expense Tracker</strong><br>
                    Version 1.0.0
                </p>
                <p style="color: #6b7280; font-size: 13px; margin: 0;">
                    A simple, clean expense tracking application built with Python and Streamlit. 
                    All data is stored locally in a JSON file.
                </p>
            </div>
        """, unsafe_allow_html=True)


# ============================================
# MAIN APP
# ============================================

def main():
    """Main application entry point."""
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Route to appropriate page
    if page == "Dashboard":
        page_dashboard()
    elif page == "Add Income":
        page_add_income()
    elif page == "Add Expense":
        page_add_expense()
    elif page == "Reports":
        page_reports()
    elif page == "Settings":
        page_settings()


if __name__ == "__main__":
    main()