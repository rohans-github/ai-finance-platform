# =============================================================================
# File: app.py (Main Flask Backend)
# =============================================================================

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)
CORS(app)

# Database setup
DATABASE = 'finance_tracker.db'

@contextmanager
def get_db():
    """Database context manager"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
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
            emergency_fund_target = monthly_expenses * 3
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

# API Routes
@app.route('/')
def index():
    """Serve the main application"""
    return render_template('index.html')

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
    weekly_data = []
    for week in range(4):
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
    print("- Professional project structure")
    print("- Persistent data storage")
    app.run(debug=True, port=5000)
