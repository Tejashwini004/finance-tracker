import sqlite3

DATABASE = 'finance.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def add_transaction(type, amount, category, description, date):
    conn = get_db()
    conn.execute(
        'INSERT INTO transactions (type, amount, category, description, date) VALUES (?, ?, ?, ?, ?)',
        (type, amount, category, description, date)
    )
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = get_db()
    transactions = conn.execute(
        'SELECT * FROM transactions ORDER BY date DESC'
    ).fetchall()
    conn.close()
    return transactions

def get_summary():
    conn = get_db()
    income = conn.execute(
        'SELECT SUM(amount) FROM transactions WHERE type = "income"'
    ).fetchone()[0] or 0
    expenses = conn.execute(
        'SELECT SUM(amount) FROM transactions WHERE type = "expense"'
    ).fetchone()[0] or 0
    conn.close()
    return {
        'income': income,
        'expenses': expenses,
        'balance': income - expenses
    }

def get_category_totals():
    conn = get_db()
    totals = conn.execute(
        'SELECT category, SUM(amount) as total FROM transactions WHERE type = "expense" GROUP BY category'
    ).fetchall()
    conn.close()
    return totals