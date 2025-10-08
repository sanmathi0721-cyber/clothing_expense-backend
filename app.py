from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            item TEXT,
            price REAL,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        item = request.form['item']
        price = request.form['price']
        category = request.form['category']
        date = request.form['date']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (item, price, category, date) VALUES (?, ?, ?, ?)",
                  (item, price, category, date))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_expense.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
