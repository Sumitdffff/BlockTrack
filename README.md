# 🔗 BlockTrack – Blockchain-Based Transaction Tracker

**BlockTrack** is a Python-based financial transaction tracking application that uses **SHA-256 hashing** to maintain transaction integrity. It records income and expenses, links transactions using previous hashes, and detects unauthorized changes through blockchain-style verification.

The application provides an interactive dashboard to manage transactions, analyze weekly spending, view transaction history, and verify the integrity of individual records or the entire chain.

---

## 🖥️ Project Overview

BlockTrack is built using **Python and Streamlit**, providing a modern, interactive dashboard with a premium dark glassmorphism interface.

### Highlights:
- ✔ Blockchain-style transaction tracking using SHA-256
- ✔ Income and expense management
- ✔ Automatic generation of current and previous hashes
- ✔ Individual transaction integrity verification
- ✔ Full-chain verification to detect data tampering
- ✔ Interactive financial dashboard and charts
- ✔ Weekly income and expense analysis
- ✔ Searchable and filterable transaction history
- ✔ CSV-based data storage

---

## 🚀 Features

### 💰 Transaction Management
- Add income and expense transactions
- Record transaction ID, date, amount, category, payment method, and description
- Validate transaction details before saving
- Prevent duplicate transaction IDs
- Automatically link new transactions to the previous transaction hash

### 🔐 Blockchain Verification
- Uses the SHA-256 hashing algorithm
- Generates a unique hash for each transaction record
- Stores the previous transaction's hash to establish a chain
- Verifies individual transactions using their ID and expected amount
- Checks hash integrity and previous-hash links
- Detects modifications to transaction data

### 📊 Financial Dashboard
- Displays total income, total expenses, and net balance
- Shows the total number of transactions
- Visualizes expenses by category using pie charts
- Displays daily expenses and cumulative spending trends
- Compares income and expenses using interactive charts

### 📋 Transaction History
- View all recorded transactions
- Filter transactions by income or expense
- Filter by transaction category
- Search transactions using descriptions
- Filter records by date range
- View total income, expenses, and net balance for filtered records

### 📆 Weekly Analysis
- Select any date to analyze its corresponding week
- Calculate weekly income and expenses
- Display weekly net balance and transaction count
- Visualize category-wise expenses
- Analyze daily expenses from Monday to Sunday
- View all transactions recorded during the selected week

### 🎨 User Interface
- Modern dark glassmorphism theme
- Interactive Streamlit components
- Responsive dashboard layout
- Custom-styled buttons, cards, tables, and charts
- Sidebar navigation for easy access to all modules

---

## 🛠️ Tech Stack

### Programming Language
- Python 3.8+

### Frontend and Dashboard
- Streamlit
- HTML
- CSS

### Data Processing and Visualization
- Pandas
- Plotly Express

### Security and Data Integrity
- SHA-256 hashing using Python's `hashlib`
- Hash chaining using current and previous hashes

### Data Storage
- CSV (`transactions.csv`)

### Tools Used
- Visual Studio Code
- Python
- pip
- Git and GitHub

---

## 📦 Modules Included

### 📊 Dashboard Module
Displays financial summaries, transaction statistics, and interactive charts for understanding income and spending patterns.

### ➕ Add Transaction Module
Allows users to add new income or expense records after validating the transaction details. Each new record receives a SHA-256 hash and a reference to the previous record's hash.

### 📋 Transaction History Module
Displays transaction records with filtering options for transaction type, category, description, and date range.

### 📆 Weekly Analysis Module
Analyzes income, expenses, and balance for a selected week and presents the results through interactive charts and transaction tables.

### 🔐 Blockchain Verification Module
Provides individual transaction verification and full-chain verification by recalculating hashes and checking previous-hash links.

### 💾 CSV Storage Module
Stores transaction records in `transactions.csv`, including transaction details, current hashes, and previous hashes.

---

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.8 or later
- pip package manager
- Git (optional, for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/BlockTrack.git
cd BlockTrack
```

Replace `YOUR_USERNAME` with your GitHub username and `BlockTrack` with your repository name if different.

### Step 2: Install Dependencies

```bash
pip install streamlit pandas plotly
```

### Step 3: Run the Application

Save the Python code as `app.py` and run:

```bash
streamlit run app.py
```

The application will open in your browser. If it does not open automatically, visit:

```text
http://localhost:8501
```

---

## 📁 Project Structure

```text
BlockTrack/
│
├── app.py
├── transactions.csv
├── README.md
└── requirements.txt
```

**Note:** The application automatically creates `transactions.csv` if it does not exist. The file stores transaction data locally. Include it in the repository only if you intentionally want to share sample records.

---

## 🔒 How Blockchain Verification Works

1. **Genesis Hash:** The first transaction uses a predefined hash consisting of 64 zeros as its previous hash.
2. **Transaction Hash:** The application generates a SHA-256 hash from the transaction details and previous hash.
3. **Hash Linking:** Each new transaction stores the hash of the preceding transaction.
4. **Integrity Verification:** The application recalculates the hash and compares it with the stored hash.
5. **Chain Verification:** The application checks whether each transaction's previous hash matches the preceding transaction's stored hash.
6. **Tampering Detection:** If transaction data or hash links are modified, verification can identify the inconsistency.

**Important:** This is an educational blockchain-style demonstration, not a real decentralized blockchain. Because the records are stored in a local CSV file, this system does not provide distributed consensus or protection against an attacker who can rewrite the entire file and recompute all hashes.

---

## 🎯 Purpose of the Project

- Demonstrates blockchain-style transaction integrity using SHA-256.
- Provides practical experience with Python and Streamlit.
- Implements financial record management and data validation.
- Demonstrates hash chaining and tampering detection.
- Uses Pandas for data processing and Plotly for interactive visualization.
- Serves as an academic project for learning blockchain concepts and financial analytics.

---

## 🔮 Future Enhancements

- User authentication and role-based access control
- MySQL or MongoDB database integration
- Export transaction reports to Excel and PDF
- Budget management and spending alerts
- Advanced financial analytics
- Real blockchain integration using Ethereum or another blockchain platform
- Digital signatures for transaction authentication
- Cloud deployment and secure remote access

  
