from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_transaction, get_all_transactions, get_summary, get_category_totals

app = Flask(__name__)

# Initialize database when app starts
with app.app_context():
    init_db()

@app.route('/')
def index():
    transactions = get_all_transactions()
    summary = get_summary()
    category_totals = get_category_totals()
    
    # Prepare chart data
    categories = [row['category'] for row in category_totals]
    amounts = [row['total'] for row in category_totals]
    
    return render_template('index.html', 
        transactions=transactions,
        summary=summary,
        categories=categories,
        amounts=amounts
    )

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        type = request.form['type']
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']
        add_transaction(type, amount, category, description, date)
        return redirect(url_for('index'))
    return render_template('add_transaction.html')

@app.route('/summary')
def summary():
    summary = get_summary()
    category_totals = get_category_totals()
    return render_template('summary.html',
        summary=summary,
        category_totals=category_totals
    )

if __name__ == '__main__':
    app.run(debug=True)