from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from version import version
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers_data")
    customers = cur.fetchall()
    return render_template('index.html', customers=customers)

@app.route('/customer/new', methods=['GET', 'POST'])
def new_customer():
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()
        customer = (
            request.form['name'],
            request.form['phone'],
            request.form['address'],
            request.form['contact']
        )
        cur.execute("INSERT INTO customers_data (name, phone, address, contact) VALUES (?, ?, ?, ?)", customer)
        conn.commit()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('new_customer.html')

@app.route('/customer/edit/<id>', methods=['GET', 'POST'])
def edit_customer(id):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        updated_customer = (
            request.form['name'],
            request.form['phone'],
            request.form['address'],
            request.form['contact'],
            id
        )
        cur.execute("UPDATE customers_data SET name = ?, phone = ?, address = ?, contact = ? WHERE id = ?", updated_customer)
        conn.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('index'))
    cur.execute("SELECT * FROM customers_data WHERE id = ?", (id,))
    customer = cur.fetchone()
    return render_template('edit_customer.html', customer=customer)

@app.route('/customer/delete/<id>', methods=['POST'])
def delete_customer(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM customers_data WHERE id = ?", (id,))
    conn.commit()
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/actuator/info', methods=['GET', 'POST'])
def info():
    return jsonify({"build": {"version": version}})

if __name__ == "__main__":
    init_db()  # Initialize the database before starting the app
    app.run(host="0.0.0.0", port=5000, debug=True)
