# BlockTrack — Blockchain-Based Transaction Tracker

> A simple, academic project that demonstrates blockchain-inspired transaction tracking using Python, CSV, and Streamlit.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Blockchain Concepts Used](#blockchain-concepts-used)
5. [Project Structure](#project-structure)
6. [Installation & Setup](#installation--setup)
7. [Running the App](#running-the-app)
8. [How to Use](#how-to-use)
9. [Sample Test Cases](#sample-test-cases)
10. [Viva / Presentation Notes](#viva--presentation-notes)

---

## Project Overview

**BlockTrack** is a beginner-friendly, blockchain-inspired financial transaction tracker built as a college academic project.

It lets you:
- Record income and expense transactions.
- Store them persistently in a CSV file.
- Link records using SHA-256 hashes (inspired by blockchain).
- Detect whether any record has been tampered with.
- Analyse weekly finances and view charts on a dashboard.

> **Note:** BlockTrack is NOT a real blockchain or cryptocurrency application. It does not use Ethereum, Solidity, Web3, MetaMask, or any crypto wallet. It only demonstrates the hashing and hash-linking concept that real blockchains use, implemented in pure Python.

---

## Features

| Feature | Description |
|---|---|
| **Add Transaction** | Enter income or expense details; they are validated and saved with a SHA-256 hash |
| **CSV Storage** | All transactions are stored in `transactions.csv`; data persists after restart |
| **Blockchain Hashing** | Each transaction carries a SHA-256 hash and links to the previous hash |
| **Transaction History** | View, search, and filter all transactions |
| **Weekly Analysis** | Income, expenses, balance, and charts for any selected week |
| **Dashboard** | 4 summary cards + 4 interactive Plotly charts |
| **Verify Blockchain** | Re-compute every hash and detect any tampered or unlinked records |

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.8+ |
| UI Framework | Streamlit |
| Data Storage | CSV (built-in `csv` module) |
| Hashing | SHA-256 via `hashlib` (built-in) |
| Data Analysis | Pandas |
| Charts | Plotly Express |
| Date Handling | `datetime` (built-in) |

No database (SQLite, MySQL, MongoDB) is used. CSV is the sole persistent storage.

---

## Blockchain Concepts Used

### 1. SHA-256 Hashing
Every transaction is assigned a unique hash computed with Python's built-in `hashlib.sha256()`. The hash is derived from all the transaction fields concatenated with a `|` delimiter.

```
hash = SHA256(id | date | type | amount | category | payment_method | description | previous_hash)
```

### 2. Hash Chaining (Previous Hash)
Each transaction stores the hash of the **preceding** transaction as its `previous_hash`. The very first transaction uses a genesis value of 64 zeros (`"000...0"`). This creates a chain:

```
Genesis (0000...0)
    ↓
TXN0001  [prev=0000...0]  → hash_A
    ↓
TXN0002  [prev=hash_A]   → hash_B
    ↓
TXN0003  [prev=hash_B]   → hash_C
```

### 3. Tamper Detection
When **Verify Blockchain** is clicked, the app:
1. Reads every record in order.
2. Recomputes its hash from stored fields.
3. Compares the recomputed hash with the stored `current_hash`.
4. Checks that the stored `previous_hash` matches the preceding record's `current_hash`.

If a record is manually edited in the CSV, its hash will no longer match — and the verification will report a **FAIL** for that record.

---

## Project Structure

```
BlockTrack/
│
├── app.py              ← Main application (all logic in one file)
├── transactions.csv    ← Persistent transaction storage
├── requirements.txt    ← External Python dependencies
└── README.md           ← This file
```

### `app.py` — Function Reference

| Function | Purpose |
|---|---|
| `compute_hash(...)` | Computes SHA-256 hash from transaction fields |
| `initialize_csv()` | Creates `transactions.csv` with headers if it doesn't exist |
| `load_transactions()` | Reads CSV into a Pandas DataFrame |
| `save_transaction(record)` | Appends a single record to the CSV |
| `get_last_hash()` | Returns the latest `current_hash` (or genesis) |
| `transaction_id_exists(tx_id)` | Checks for duplicate IDs |
| `validate_transaction(...)` | Returns a list of validation errors |
| `verify_blockchain()` | Verifies hash integrity for all records |
| `get_week_bounds(date)` | Returns Monday–Sunday for a given date |
| `weekly_summary(df, start, end)` | Computes weekly stats and chart data |
| `seed_sample_data()` | Seeds 5 sample transactions on first run |
| `page_dashboard(df)` | Renders the Dashboard page |
| `page_add_transaction()` | Renders the Add Transaction page |
| `page_transaction_history(df)` | Renders the History page |
| `page_weekly_analysis(df)` | Renders the Weekly Analysis page |
| `page_verify_blockchain(df)` | Renders the Verify Blockchain page |
| `main()` | Entry point; sets up Streamlit layout and routing |

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher ([download](https://www.python.org/downloads/))
- pip (bundled with Python)

### Steps

**1. Open a terminal / PowerShell in the project folder**

```powershell
cd e:\sumit\bc
```

**2. (Optional but recommended) Create a virtual environment**

```powershell
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```powershell
pip install -r requirements.txt
```

---

## Running the App

```powershell
streamlit run app.py
```

Streamlit will print a local URL such as:

```
Local URL: http://localhost:8501
```

Open that URL in your browser.

> On first launch, `transactions.csv` is automatically populated with 5 sample transactions so you can explore the dashboard immediately.

---

## How to Use

### Dashboard
- View total income, expenses, net balance, and transaction count.
- Four charts update automatically as you add transactions.

### Add Transaction
1. Fill in the form (ID, date, type, amount, category, payment method, description).
2. Click **Save Transaction**.
3. The generated SHA-256 hash and the linked previous hash are displayed.

### Transaction History
- Use the **Type**, **Category**, and **Date** filters to narrow results.
- Use the **Search** box to find transactions by keyword.

### Weekly Analysis
- Pick any date within the week you want to analyse.
- View income, expenses, balance, category pie chart, and daily bar chart.

### Verify Blockchain
- Click **Verify Transaction Integrity**.
- Each transaction shows **PASS** (green) or **FAIL** (red).
- If you manually edit `transactions.csv` and change any field, the affected row will fail.

---

## Sample Test Cases

### Test 1 — Add a Transaction
1. Go to **Add Transaction**.
2. Enter: ID=`TXN0010`, Date=today, Type=`Income`, Amount=`2000`, Category=`Freelance`, Payment=`UPI`, Description=`Test income`.
3. Click **Save Transaction**.
4. Expected: Success message with a 64-character SHA-256 hash displayed.
5. Verify: Go to **Transaction History** and confirm `TXN0010` appears.

### Test 2 — Calculate Weekly Report
1. Go to **Weekly Analysis**.
2. Select a date in the week of 12 Oct 2026 (sample data week).
3. Expected:
   - Weekly Income = Rs 6,000 (Salary 5000 + Freelance 1000)
   - Weekly Expenses = Rs 1,050 (Food 250 + Travel 500 + Shopping 300)
   - Weekly Balance = Rs 4,950

### Test 3 — Detect Tampering
1. Open `transactions.csv` in Notepad or Excel.
2. Change the `amount` of `TXN0001` from `5000.0` to `9999.0`.
3. Save the file.
4. Go to **Verify Blockchain** and click **Verify Transaction Integrity**.
5. Expected: `TXN0001` shows **FAIL** — hash mismatch detected.

### Test 4 — Duplicate Transaction ID
1. Go to **Add Transaction**.
2. Enter ID=`TXN0001` (already exists in sample data).
3. Click **Save Transaction**.
4. Expected: Error message — "Transaction ID 'TXN0001' already exists."

### Test 5 — Invalid Amount
1. Go to **Add Transaction**.
2. Enter Amount=`-100`.
3. Click **Save Transaction**.
4. Expected: Error message — "Amount must be a positive number."

---

## Viva / Presentation Notes

**Q: What is a blockchain?**
A: A blockchain is a chain of data blocks where each block contains data and a hash of the previous block. This makes it tamper-evident because changing any block invalidates all subsequent hashes.

**Q: How does BlockTrack use blockchain concepts?**
A: Every transaction is treated like a block. Each transaction contains its own SHA-256 hash (computed from its data) and the hash of the previous transaction. If any record is modified, its hash changes and the chain breaks.

**Q: What hashing algorithm is used?**
A: SHA-256 (Secure Hash Algorithm 256-bit), provided by Python's built-in `hashlib` library.

**Q: Why CSV instead of a database?**
A: CSV is simpler, human-readable, and requires no external database installation — ideal for a beginner academic project.

**Q: Is this a real blockchain?**
A: No. It is an educational simulation. It does not involve decentralisation, consensus algorithms, peer-to-peer networks, or cryptocurrency. It only demonstrates the hash-chaining concept.

**Q: What happens when a transaction is tampered with?**
A: The Verify Blockchain page recomputes every hash. If a stored hash doesn't match the recomputed hash, or if the `previous_hash` field doesn't match the preceding transaction's hash, the record is flagged as **FAIL**.

---

*BlockTrack — Academic Project | Python + Streamlit + CSV + SHA-256*
