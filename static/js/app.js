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
