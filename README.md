# Full Stack AI Finance Tracker - Rohan Chadha (CS4365)

A full-stack personal finance management application with AI-powered insights, built with Python Flask backend and modern frontend technologies.

![AI Finance Tracker](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-orange.svg)

## ✨ Features

### 🎯 Core Functionality
- **Transaction Management** - Track income and expenses with categories
- **Budget Setting & Monitoring** - Set monthly budgets and track usage
- **Real-time Dashboard** - Live financial overview with key metrics
- **Data Persistence** - SQLite database for permanent data storage

### 🤖 AI-Powered Insights
- **Smart Financial Analysis** - Automated spending pattern detection
- **Budget Alerts** - Intelligent warnings for overspending
- **Savings Recommendations** - Personalized advice based on your data
- **Trend Analysis** - Weekly spending comparisons and insights
- **Emergency Fund Planning** - Automated recommendations for financial security

### 🎨 Modern Interface
- **Responsive Design** - Works perfectly on desktop and mobile
- **Interactive Dashboard** - Real-time updates and smooth animations
- **Professional UI** - Clean, modern design with intuitive navigation
- **Visual Feedback** - Progress bars, notifications, and status indicators

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-finance-platform.git
   cd ai-finance-platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
ai-finance-tracker/
│
├── app.py                 # Flask backend with API routes
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
│
├── templates/
│   └── index.html        # HTML template
│
├── static/
│   ├── css/
│   │   └── style.css     # Styling and animations
│   └── js/
│       └── app.js        # Frontend JavaScript logic
│
└── finance_tracker.db    # SQLite database (auto-created)
```

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 3.0.0** - Web framework
- **SQLite** - Database for data persistence
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Structure and semantic markup
- **CSS3** - Modern styling with animations and gradients
- **JavaScript (ES6+)** - Interactive functionality and API communication
- **Fetch API** - Asynchronous data operations

### Database Schema
```sql
-- Transactions table
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    type TEXT CHECK(type IN ('income', 'expense')),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Budgets table
CREATE TABLE budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT UNIQUE NOT NULL,
    amount REAL NOT NULL,
    period TEXT DEFAULT 'monthly',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📊 API Endpoints

### Transactions
- `GET /api/transactions` - Retrieve transactions
- `POST /api/transactions` - Add new transaction

### Budgets
- `GET /api/budgets` - Get all budgets
- `POST /api/budgets` - Set/update budget

### Analytics
- `GET /api/summary` - Financial summary data
- `GET /api/ai-advice` - AI-generated insights
- `GET /api/analytics` - Advanced analytics data

## 🤖 AI Features

The AI system analyzes your financial data to provide:

1. **Spending Alerts** - Notifications when approaching budget limits
2. **Savings Rate Analysis** - Recommendations for optimal savings
3. **Category Insights** - Identify highest spending areas
4. **Trend Detection** - Weekly spending pattern analysis
5. **Emergency Fund Planning** - Automated recommendations based on expenses
6. **Behavioral Insights** - Transaction frequency and pattern analysis

## 🎨 Screenshots

### Dashboard
- Real-time financial overview
- Monthly income vs expenses
- Recent transactions list
- Budget progress indicators

### AI Insights
- Personalized financial advice
- Budget alerts and warnings
- Savings recommendations
- Trend analysis

## 🔧 Configuration

### Environment Variables
The application runs with default settings. For production deployment, consider:

- `FLASK_ENV=production`
- `DATABASE_URL` - Custom database location
- `SECRET_KEY` - Flask secret key for sessions

### Database
SQLite database is automatically created on first run. The database file (`finance_tracker.db`) stores:
- All transactions (income/expenses)
- Budget settings
- Category definitions

## Acknowledgments

- Flask framework for the robust backend
- SQLite for reliable data storage
- Modern CSS techniques for the beautiful interface
- AI algorithms for intelligent financial insights
