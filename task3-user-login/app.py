from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Render PostgreSQL config
DB_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DB_URL)

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        conn.close()

        msg = 'Registration successful!'

    return render_template('register.html', message=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return render_template('success.html', username=username)
        else:
            msg = 'Invalid username or password'

    return render_template('login.html', message=msg)

if __name__ == '__main__':
    app.run(debug=True)
