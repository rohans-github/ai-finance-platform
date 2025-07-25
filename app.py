# app.py - Complete Single-File Flask Backend with Embedded Frontend
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Database setup
DATABASE = 'finance_tracker.db'

@contextmanager
def get_db():
    """Database context manager"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize the database with required tables"""
    with get_db() as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT UNIQUE NOT NULL,
                amount REAL NOT NULL,
                period TEXT DEFAULT 'monthly',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        ''')
        
        # Insert default categories
        default_categories = ['Food', 'Transportation', 'Entertainment', 'Utilities', 'Healthcare', 'Shopping', 'Other']
        for category in default_categories:
            conn.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (category,))
        
        conn.commit()

class AIFinanceTracker:
    """Enhanced AI Finance Tracker with database integration"""
    
    @staticmethod
    def add_transaction(amount, category, description, transaction_type):
        """Add a new transaction to the database"""
        with get_db() as conn:
            conn.execute(
                'INSERT INTO transactions (amount, category, description, type) VALUES (?, ?, ?, ?)',
                (float(amount), category, description, transaction_type)
            )
            conn.commit()
            return {"success": True, "message": f"{transaction_type.capitalize()} of ${amount} added successfully!"}
    
    @staticmethod
    def get_transactions(limit=None, days=None):
        """Get transactions with optional filters"""
        query = 'SELECT * FROM transactions'
        params = []
        
        if days:
            query += ' WHERE date >= ?'
            params.append((datetime.now() - timedelta(days=days)).isoformat())
        
        query += ' ORDER BY date DESC'
        
        if limit:
            query += ' LIMIT ?'
            params.append(limit)
        
        with get_db() as conn:
            return [dict(row) for row in conn.execute(query, params).fetchall()]
    
    @staticmethod
    def set_budget(category, amount):
        """Set or update budget for a category"""
        with get_db() as conn:
            conn.execute(
                'INSERT OR REPLACE INTO budgets (category, amount) VALUES (?, ?)',
                (category, float(amount))
            )
            conn.commit()
            return {"success": True, "message": f"Budget set: ${amount} for {category}"}
    
    @staticmethod
    def get_budgets():
        """Get all budgets"""
        with get_db() as conn:
            return [dict(row) for row in conn.execute('SELECT * FROM budgets').fetchall()]
    
    @staticmethod
    def get_spending_by_category(days=30):
        """Get spending breakdown by category for the last N days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with get_db() as conn:
            rows = conn.execute('''
                SELECT category, SUM(amount) as total
                FROM transactions 
                WHERE type = 'expense' AND date >= ?
                GROUP BY category
            ''', (cutoff_date,)).fetchall()
            
            return {row['category']: row['total'] for row in rows}
    
    @staticmethod
    def get_income_vs_expenses(days=30):
        """Calculate total income vs expenses for the last N days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with get_db() as conn:
            result = conn.execute('''
                SELECT 
                    type,
                    SUM(amount) as total
                FROM transactions 
                WHERE date >= ?
                GROUP BY type
            ''', (cutoff_date,)).fetchall()
            
            income = 0
            expenses = 0
            for row in result:
                if row['type'] == 'income':
                    income = row['total']
                elif row['type'] == 'expense':
                    expenses = row['total']
            
            return {"income": income, "expenses": expenses}
    
    @staticmethod
    def get_budget_status():
        """Check budget status for all categories"""
        spending = AIFinanceTracker.get_spending_by_category(30)
        budgets = AIFinanceTracker.get_budgets()
        
        status = {}
        for budget in budgets:
            category = budget['category']
            spent = spending.get(category, 0)
            budget_amount = budget['amount']
            percentage_used = (spent / budget_amount) * 100 if budget_amount > 0 else 0
            
            status[category] = {
                "spent": spent,
                "budget": budget_amount,
                "remaining": budget_amount - spent,
                "percentage_used": percentage_used
            }
        
        return status
    
    @staticmethod
    def generate_ai_advice():
        """Generate comprehensive AI-powered financial insights"""
        advice = []
        
        # Get financial data
        income_expenses = AIFinanceTracker.get_income_vs_expenses(30)
        income = income_expenses["income"]
        expenses = income_expenses["expenses"]
        spending_by_category = AIFinanceTracker.get_spending_by_category(30)
        budget_status = AIFinanceTracker.get_budget_status()
        recent_transactions = AIFinanceTracker.get_transactions(days=7)
        
        # Financial health analysis
        if expenses > income and income > 0:
            deficit = expenses - income
            advice.append({
                "type": "alert",
                "icon": "🚨",
                "message": f"ALERT: You're spending ${deficit:.2f} more than you earn this month!",
                "suggestion": "Consider reducing discretionary expenses or finding additional income sources."
            })
        elif income > expenses and income > 0:
            surplus = income - expenses
            advice.append({
                "type": "positive",
                "icon": "🎉", 
                "message": f"Great job! You have a surplus of ${surplus:.2f} this month.",
                "suggestion": "Consider saving or investing this extra money for future goals."
            })
        
        # Budget analysis with advanced insights
        for category, status in budget_status.items():
            if status["percentage_used"] > 100:
                overspend = status["spent"] - status["budget"]
                advice.append({
                    "type": "warning",
                    "icon": "🚨",
                    "message": f"Over budget in {category} by ${overspend:.2f}",
                    "suggestion": f"You've used {status['percentage_used']:.1f}% of your {category} budget. Consider cutting back on non-essential {category.lower()} expenses."
                })
            elif status["percentage_used"] > 80:
                advice.append({
                    "type": "caution",
                    "icon": "⚡",
                    "message": f"Close to {category} budget limit ({status['percentage_used']:.1f}% used)",
                    "suggestion": f"You have ${status['remaining']:.2f} left in your {category} budget. Plan carefully for the rest of the month."
                })
        
        # Spending pattern analysis
        if spending_by_category:
            top_category = max(spending_by_category, key=spending_by_category.get)
            top_amount = spending_by_category[top_category]
            
            advice.append({
                "type": "info",
                "icon": "📊",
                "message": f"Your highest spending category is {top_category} (${top_amount:.2f})",
                "suggestion": f"This represents {(top_amount/expenses*100):.1f}% of your total expenses." if expenses > 0 else ""
            })
            
            # Category-specific advice
            if income > 0 and top_amount > income * 0.3:
                advice.append({
                    "type": "insight",
                    "icon": "💭",
                    "message": f"Your {top_category} spending is high relative to income",
                    "suggestion": f"Consider if {top_amount:.2f} on {top_category} aligns with your financial priorities."
                })
        
        # Savings recommendations with specific targets
        if income > 0:
            savings_rate = ((income - expenses) / income) * 100
            if savings_rate < 0:
                advice.append({
                    "type": "urgent",
                    "icon": "🆘",
                    "message": "Negative savings rate - spending exceeds income",
                    "suggestion": "Create an emergency budget focusing only on essential expenses."
                })
            elif savings_rate < 10:
                target_savings = income * 0.10
                advice.append({
                    "type": "goal",
                    "icon": "💰",
                    "message": f"Current savings rate: {savings_rate:.1f}%",
                    "suggestion": f"Aim to save ${target_savings:.2f} monthly (10% of income) for financial security."
                })
            elif savings_rate >= 20:
                advice.append({
                    "type": "excellent",
                    "icon": "🌟",
                    "message": f"Excellent savings rate of {savings_rate:.1f}%!",
                    "suggestion": "Consider diversifying investments or increasing emergency fund contributions."
                })
        
        # Transaction behavior insights
        if len(recent_transactions) > 20:
            daily_avg = len(recent_transactions) / 7
            advice.append({
                "type": "behavioral",
                "icon": "📱",
                "message": f"High transaction frequency: {len(recent_transactions)} transactions this week",
                "suggestion": f"Averaging {daily_avg:.1f} transactions per day. Consider consolidating purchases to reduce impulse spending."
            })
        
        # Emergency fund recommendation
        monthly_expenses = expenses
        if monthly_expenses > 0:
            emergency_fund_target = monthly_expenses * 3  # 3 months of expenses
            advice.append({
                "type": "planning",
                "icon": "🛡️",
                "message": "Emergency Fund Recommendation",
                "suggestion": f"Based on your monthly expenses (${monthly_expenses:.2f}), aim for an emergency fund of ${emergency_fund_target:.2f} (3 months of expenses)."
            })
        
        # If no specific advice, provide encouragement
        if not advice:
            advice.append({
                "type": "encouragement",
                "icon": "💡",
                "message": "Keep tracking your finances!",
                "suggestion": "More insights will be available as you add more transaction data. You're building great financial habits!"
            })
        
        return advice

# Frontend HTML embedded in Python
HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Finance Tracker - Full Stack</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .status-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 10px;
            backdrop-filter: blur(10px);
        }

        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }

        .card h3 {
            color: #4a5568;
            margin-bottom: 20px;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #4a5568;
        }

        .form-group input,
        .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .summary-item {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }

        .summary-item.positive {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }

        .summary-item.negative {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }

        .summary-item h4 {
            font-size: 0.9rem;
            margin-bottom: 8px;
            opacity: 0.9;
        }

        .summary-item .amount {
            font-size: 1.8rem;
            font-weight: bold;
        }

        .transaction-list {
            max-height: 400px;
            overflow-y: auto;
        }

        .transaction-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            border-bottom: 1px solid #e2e8f0;
            transition: background-color 0.3s ease;
        }

        .transaction-item:hover {
            background-color: #f7fafc;
        }

        .transaction-info {
            flex: 1;
        }

        .transaction-category {
            font-weight: 600;
            color: #4a5568;
        }

        .transaction-description {
            font-size: 0.9rem;
            color: #718096;
            margin-top: 2px;
        }

        .transaction-amount {
            font-weight: bold;
            font-size: 1.1rem;
        }

        .transaction-amount.income {
            color: #38a169;
        }

        .transaction-amount.expense {
            color: #e53e3e;
        }

        .budget-item {
            padding: 15px;
            border-bottom: 1px solid #e2e8f0;
        }

        .budget-progress {
            width: 100%;
            height: 8px;
            background-color: #e2e8f0;
            border-radius: 4px;
            margin-top: 8px;
            overflow: hidden;
        }

        .budget-progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #38a169, #68d391);
            transition: width 0.3s ease;
        }

        .budget-progress-bar.warning {
            background: linear-gradient(90deg, #d69e2e, #f6e05e);
        }

        .budget-progress-bar.danger {
            background: linear-gradient(90deg, #e53e3e, #fc8181);
        }

        .ai-advice {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            margin-top: 20px;
        }

        .ai-advice h3 {
            margin-bottom: 20px;
            font-size: 1.5rem;
        }

        .advice-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            backdrop-filter: blur(10px);
            border-left: 4px solid rgba(255,255,255,0.3);
        }

        .advice-item:last-child {
            margin-bottom: 0;
        }

        .advice-item.alert {
            border-left-color: #fc8181;
            background: rgba(252, 129, 129, 0.1);
        }

        .advice-item.positive {
            border-left-color: #68d391;
            background: rgba(104, 211, 145, 0.1);
        }

        .advice-item.warning {
            border-left-color: #f6e05e;
            background: rgba(246, 224, 94, 0.1);
        }

        .advice-header {
            font-weight: bold;
            font-size: 1.1rem;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .advice-suggestion {
            font-size: 0.95rem;
            opacity: 0.9;
            line-height: 1.4;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #38a169;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            transform: translateX(400px);
            transition: transform 0.3s ease;
            z-index: 1000;
        }

        .notification.show {
            transform: translateX(0);
        }

        .notification.error {
            background: #e53e3e;
        }

        .tabs {
            display: flex;
            margin-bottom: 20px;
            background: white;
            border-radius: 10px;
            padding: 5px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .tab {
            flex: 1;
            padding: 15px;
            text-align: center;
            background: transparent;
            border: none;
            cursor: pointer;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #718096;
        }

        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #e2e8f0;
            border-radius: 50%;
            border-top-color: #667eea;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .dashboard {
                grid-template-columns: 1fr;
            }
            
            .container {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Finance Tracker</h1>
            <p>Full-Stack Python + Frontend with Advanced AI Analytics</p>
            <div class="status-badge" id="connectionStatus">🔗 Rohan Chadha (CS4365)</div>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab('dashboard')">📊 Dashboard</button>
            <button class="tab" onclick="showTab('transactions')">💰 Add Transaction</button>
            <button class="tab" onclick="showTab('budgets')">🎯 Budgets</button>
            <button class="tab" onclick="showTab('insights')">🤖 AI Insights</button>
        </div>

        <!-- Dashboard Tab -->
        <div id="dashboard" class="tab-content active">
            <div class="summary-grid">
                <div class="summary-item positive">
                    <h4>Monthly Income</h4>
                    <div class="amount" id="monthlyIncome">$0.00</div>
                </div>
                <div class="summary-item negative">
                    <h4>Monthly Expenses</h4>
                    <div class="amount" id="monthlyExpenses">$0.00</div>
                </div>
                <div class="summary-item">
                    <h4>Net Balance</h4>
                    <div class="amount" id="netBalance">$0.00</div>
                </div>
                <div class="summary-item">
                    <h4>Savings Rate</h4>
                    <div class="amount" id="savingsRate">0%</div>
                </div>
            </div>

            <div class="dashboard">
                <div class="card">
                    <h3>📋 Recent Transactions</h3>
                    <div class="transaction-list" id="recentTransactions">
                        <div class="loading">
                            <div class="spinner"></div> Loading transactions...
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h3>🎯 Budget Overview</h3>
                    <div id="budgetOverview">
                        <div class="loading">
                            <div class="spinner"></div> Loading budgets...
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Transactions Tab -->
        <div id="transactions" class="tab-content">
            <div class="dashboard">
                <div class="card">
                    <h3>💸 Add Expense</h3>
                    <form id="expenseForm">
                        <div class="form-group">
                            <label for="expenseAmount">Amount ($)</label>
                            <input type="number" id="expenseAmount" step="0.01" required>
                        </div>
                        <div class="form-group">
                            <label for="expenseCategory">Category</label>
                            <select id="expenseCategory" required>
                                <option value="">Select category</option>
                                <option value="Food">🍽️ Food</option>
                                <option value="Transportation">🚗 Transportation</option>
                                <option value="Entertainment">🎬 Entertainment</option>
                                <option value="Utilities">⚡ Utilities</option>
                                <option value="Healthcare">🏥 Healthcare</option>
                                <option value="Shopping">🛒 Shopping</option>
                                <option value="Other">📦 Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="expenseDescription">Description</label>
                            <input type="text" id="expenseDescription" required>
                        </div>
                        <button type="submit" class="btn">Add Expense</button>
                    </form>
                </div>

                <div class="card">
                    <h3>💰 Add Income</h3>
                    <form id="incomeForm">
                        <div class="form-group">
                            <label for="incomeAmount">Amount ($)</label>
                            <input type="number" id="incomeAmount" step="0.01" required>
                        </div>
                        <div class="form-group">
                            <label for="incomeSource">Source</label>
                            <select id="incomeSource" required>
                                <option value="">Select source</option>
                                <option value="Salary">💼 Salary</option>
                                <option value="Freelance">🛠️ Freelance</option>
                                <option value="Investment">📈 Investment</option>
                                <option value="Business">🏢 Business</option>
                                <option value="Other">💵 Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="incomeDescription">Description</label>
                            <input type="text" id="incomeDescription" required>
                        </div>
                        <button type="submit" class="btn">Add Income</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Budgets Tab -->
        <div id="budgets" class="tab-content">
            <div class="dashboard">
                <div class="card">
                    <h3>🎯 Set Budget</h3>
                    <form id="budgetForm">
                        <div class="form-group">
                            <label for="budgetCategory">Category</label>
                            <select id="budgetCategory" required>
                                <option value="">Select category</option>
                                <option value="Food">🍽️ Food</option>
                                <option value="Transportation">🚗 Transportation</option>
                                <option value="Entertainment">🎬 Entertainment</option>
                                <option value="Utilities">⚡ Utilities</option>
                                <option value="Healthcare">🏥 Healthcare</option>
                                <option value="Shopping">🛒 Shopping</option>
                                <option value="Other">📦 Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="budgetAmount">Monthly Budget ($)</label>
                            <input type="number" id="budgetAmount" step="0.01" required>
                        </div>
                        <button type="submit" class="btn">Set Budget</button>
                    </form>
                </div>

                <div class="card">
                    <h3>📊 Budget Status</h3>
                    <div id="budgetStatus">
                        <div class="loading">
                            <div class="spinner"></div> Loading budget status...
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- AI Insights Tab -->
        <div id="insights" class="tab-content">
            <div class="ai-advice">
                <h3>🤖 Advanced AI Financial Insights</h3>
                <div id="aiAdvice">
                    <div class="loading">
                        <div class="spinner"></div> Generating AI insights...
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="notification" class="notification"></div>

    <script>
        // API Configuration
        const API_BASE = '/api';
        
        // Utility Functions
        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification ${type === 'success' ? '' : 'error'} show`;
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }

        async function apiCall(endpoint, options = {}) {
            try {
                const response = await fetch(`${API_BASE}${endpoint}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    },
                    ...options
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                return await response.json();
            } catch (error) {
                console.error('API call failed:', error);
                showNotification('Connection error. Please make sure the Python backend is running.', 'error');
                document.getElementById('connectionStatus').textContent = '❌ Backend Disconnected';
                throw error;
            }
        }

        // Tab Management
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            if (tabName === 'dashboard') {
                loadDashboard();
            } else if (tabName === 'budgets') {
                loadBudgetStatus();
            } else if (tabName === 'insights') {
                loadAIInsights();
            }
        }

        // Dashboard Functions
        async function loadDashboard() {
            try {
                const summary = await apiCall('/summary');
                updateSummaryCards(summary);
                await loadRecentTransactions();
                updateBudgetOverview(summary.budget_status);
            } catch (error) {
                console.error('Failed to load dashboard:', error);
            }
        }

        function updateSummaryCards(summary) {
            const { income, expenses } = summary.income_expenses;
            const netBalance = income - expenses;
            const savingsRate = income > 0 ? ((netBalance / income) * 100) : 0;
            
            document.getElementById('monthlyIncome').textContent = `$${income.toFixed(2)}`;
            document.getElementById('monthlyExpenses').textContent = `$${expenses.toFixed(2)}`;
            document.getElementById('netBalance').textContent = `$${netBalance.toFixed(2)}`;
            document.getElementById('savingsRate').textContent = `${savingsRate.toFixed(1)}%`;
            
            const netBalanceElement = document.getElementById('netBalance').parentElement;
            netBalanceElement.className = `summary-item ${netBalance >= 0 ? 'positive' : 'negative'}`;
        }

        async function loadRecentTransactions() {
            try {
                const transactions = await apiCall('/transactions?limit=10');
                const container = document.getElementById('recentTransactions');
                
                if (transactions.length === 0) {
                    container.innerHTML = '<p style="text-align: center; color: #718096; padding: 20px;">No transactions yet. Add some to get started!</p>';
                    return;
                }
                
                container.innerHTML = transactions.map(transaction => {
                    const date = new Date(transaction.date).toLocaleDateString();
                    const emoji = transaction.type === 'income' ? '💰' : '💸';
                    
                    return `
                        <div class="transaction-item">
                            <div class="transaction-info">
                                <div class="transaction-category">${emoji} ${transaction.category}</div>
                                <div class="transaction-description">${transaction.description}</div>
                            </div>
                            <div class="transaction-amount ${transaction.type}">
                                ${transaction.type === 'income' ? '+' : '-'}$${transaction.amount.toFixed(2)}
                            </div>
                        </div>
                    `;
                }).join('');
            } catch (error) {
                document.getElementById('recentTransactions').innerHTML = '<p style="text-align: center; color: #e53e3e; padding: 20px;">Failed to load transactions</p>';
            }
        }

        function updateBudgetOverview(budgetStatus) {
            const container = document.getElementById('budgetOverview');
            const budgets = Object.keys(budgetStatus);
            
            if (budgets.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #718096; padding: 20px;">No budgets set. Create some to track your spending!</p>';
                return;
            }
            
            container.innerHTML = budgets.map(category => {
                const status = budgetStatus[category];
                const percentage = status.percentage_used;
                const remaining = status.remaining;
                
                let progressClass = '';
                if (percentage > 100) progressClass = 'danger';
                else if (percentage > 80) progressClass = 'warning';
                
                return `
                    <div class="budget-item">
                        <div style="font-weight: 600; color: #4a5568;">${category}</div>
                        <div style="font-size: 0.9rem; color: #718096; margin: 5px 0;">
                            $${status.spent.toFixed(2)} / $${status.budget.toFixed(2)} 
                            (${remaining >= 0 ? `$${remaining.toFixed(2)} left` : `$${Math.abs(remaining).toFixed(2)} over`})
                        </div>
                        <div class="budget-progress">
                            <div class="budget-progress-bar ${progressClass}" style="width: ${Math.min(percentage, 100)}%"></div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        // Transaction Functions
        async function addTransaction(type, data) {
            try {
                const result = await apiCall('/transactions', {
                    method: 'POST',
                    body: JSON.stringify({
                        ...data,
                        type: type
                    })
                });
                
                showNotification(result.message);
                loadDashboard(); // Refresh dashboard
            } catch (error) {
                showNotification(`Failed to add ${type}`, 'error');
            }
        }

        // Budget Functions
        async function setBudget(category, amount) {
            try {
                const result = await apiCall('/budgets', {
                    method: 'POST',
                    body: JSON.stringify({
                        category: category,
                        amount: parseFloat(amount)
                    })
                });
                
                showNotification(result.message);
                loadBudgetStatus();
            } catch (error) {
                showNotification('Failed to set budget', 'error');
            }
        }

        async function loadBudgetStatus() {
            try {
                const summary = await apiCall('/summary');
                const container = document.getElementById('budgetStatus');
                const budgetStatus = summary.budget_status;
                const budgets = Object.keys(budgetStatus);
                
                if (budgets.length === 0) {
                    container.innerHTML = '<p style="text-align: center; color: #718096; padding: 20px;">No budgets set yet.</p>';
                    return;
                }
                
                container.innerHTML = budgets.map(category => {
                    const status = budgetStatus[category];
                    const percentage = status.percentage_used;
                    const remaining = status.remaining;
                    
                    let progressClass = '';
                    let statusEmoji = '✅';
                    if (percentage > 100) {
                        progressClass = 'danger';
                        statusEmoji = '🚨';
                    } else if (percentage > 80) {
                        progressClass = 'warning';
                        statusEmoji = '⚠️';
                    }
                    
                    return `
                        <div class="budget-item">
                            <div style="font-weight: 600; color: #4a5568;">${statusEmoji} ${category}</div>
                            <div style="font-size: 0.9rem; color: #718096; margin: 5px 0;">
                                Spent: $${status.spent.toFixed(2)} / Budget: $${status.budget.toFixed(2)}
                            </div>
                            <div style="font-size: 0.9rem; color: #718096;">
                                ${remaining >= 0 ? 
                                    `✓ $${remaining.toFixed(2)} remaining` : 
                                    `⚠️ $${Math.abs(remaining).toFixed(2)} over budget`
                                }
                            </div>
                            <div class="budget-progress">
                                <div class="budget-progress-bar ${progressClass}" style="width: ${Math.min(percentage, 100)}%"></div>
                            </div>
                            <div style="font-size: 0.8rem; color: #718096; margin-top: 5px;">
                                ${percentage.toFixed(1)}% used
                            </div>
                        </div>
                    `;
                }).join('');
            } catch (error) {
                document.getElementById('budgetStatus').innerHTML = '<p style="text-align: center; color: #e53e3e; padding: 20px;">Failed to load budget status</p>';
            }
        }

        // AI Insights Functions
        async function loadAIInsights() {
            try {
                const advice = await apiCall('/ai-advice');
                const container = document.getElementById('aiAdvice');
                
                if (advice.length === 0) {
                    container.innerHTML = '<div class="advice-item">💡 Keep tracking your finances! More insights will be available as you add more data.</div>';
                    return;
                }
                
                container.innerHTML = advice.map(item => `
                    <div class="advice-item ${item.type}">
                        <div class="advice-header">
                            <span>${item.icon}</span>
                            <span>${item.message}</span>
                        </div>
                        ${item.suggestion ? `<div class="advice-suggestion">${item.suggestion}</div>` : ''}
                    </div>
                `).join('');
            } catch (error) {
                document.getElementById('aiAdvice').innerHTML = '<div class="advice-item">❌ Failed to load AI insights. Please check your connection.</div>';
            }
        }

        // Form Event Listeners
        document.getElementById('expenseForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Adding...';
            
            try {
                await addTransaction('expense', {
                    amount: parseFloat(document.getElementById('expenseAmount').value),
                    category: document.getElementById('expenseCategory').value,
                    description: document.getElementById('expenseDescription').value
                });
                this.reset();
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Add Expense';
            }
        });

        document.getElementById('incomeForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Adding...';
            
            try {
                await addTransaction('income', {
                    amount: parseFloat(document.getElementById('incomeAmount').value),
                    category: document.getElementById('incomeSource').value,
                    description: document.getElementById('incomeDescription').value
                });
                this.reset();
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Add Income';
            }
        });

        document.getElementById('budgetForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Setting...';
            
            try {
                await setBudget(
                    document.getElementById('budgetCategory').value,
                    document.getElementById('budgetAmount').value
                );
                this.reset();
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Set Budget';
            }
        });

        // Initialize app
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboard();
            
            // Test backend connection
            apiCall('/summary').then(() => {
                document.getElementById('connectionStatus').textContent = '🔗 Connected to Python Backend';
            }).catch(() => {
                document.getElementById('connectionStatus').textContent = '❌ Backend Disconnected';
            });
        });
    </script>
</body>
</html>'''

# API Routes
@app.route('/')
def index():
    """Serve the main application with embedded HTML"""
    return HTML_CONTENT

@app.route('/api/transactions', methods=['GET', 'POST'])
def transactions():
    """Handle transaction operations"""
    if request.method == 'POST':
        data = request.json
        result = AIFinanceTracker.add_transaction(
            data['amount'],
            data['category'], 
            data['description'],
            data['type']
        )
        return jsonify(result)
    
    # GET request
    days = request.args.get('days', type=int)
    limit = request.args.get('limit', type=int)
    transactions = AIFinanceTracker.get_transactions(limit=limit, days=days)
    return jsonify(transactions)

@app.route('/api/budgets', methods=['GET', 'POST'])
def budgets():
    """Handle budget operations"""
    if request.method == 'POST':
        data = request.json
        result = AIFinanceTracker.set_budget(data['category'], data['amount'])
        return jsonify(result)
    
    return jsonify(AIFinanceTracker.get_budgets())

@app.route('/api/summary')
def summary():
    """Get financial summary data"""
    return jsonify({
        "income_expenses": AIFinanceTracker.get_income_vs_expenses(30),
        "spending_by_category": AIFinanceTracker.get_spending_by_category(30),
        "budget_status": AIFinanceTracker.get_budget_status()
    })

@app.route('/api/ai-advice')
def ai_advice():
    """Get AI-powered financial advice"""
    return jsonify(AIFinanceTracker.generate_ai_advice())

@app.route('/api/analytics')
def analytics():
    """Get advanced analytics data"""
    # Weekly spending trend
    weekly_data = []
    for week in range(4):  # Last 4 weeks
        start_date = datetime.now() - timedelta(weeks=week+1)
        end_date = datetime.now() - timedelta(weeks=week)
        
        with get_db() as conn:
            result = conn.execute('''
                SELECT SUM(amount) as total
                FROM transactions 
                WHERE type = 'expense' 
                AND date BETWEEN ? AND ?
            ''', (start_date.isoformat(), end_date.isoformat())).fetchone()
            
            weekly_data.append({
                "week": f"Week {4-week}",
                "amount": result['total'] or 0
            })
    
    # Category trends
    category_trends = AIFinanceTracker.get_spending_by_category(30)
    
    return jsonify({
        "weekly_spending": weekly_data,
        "category_trends": category_trends
    })

if __name__ == '__main__':
    print("🚀 Initializing AI Finance Tracker...")
    init_db()
    print("✅ Database initialized successfully!")
    print("📊 Starting Flask server...")
    print("🌐 Open your browser to: http://localhost:5000")
    print("\n💡 Features:")
    print("- Python Flask backend with SQLite database")
    print("- Advanced AI analytics and insights") 
    print("- Real-time data synchronization")
    print("- Single-file deployment")
    print("- Persistent data storage")
    app.run(debug=True, port=5000)
