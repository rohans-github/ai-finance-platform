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
