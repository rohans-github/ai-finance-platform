# =============================================================================
# File: static/css/style.css (CSS Styles)
# =============================================================================

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

# =============================================================================
# File: static/js/app.js (JavaScript Logic)
# =============================================================================

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
        loadDashboard();
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
