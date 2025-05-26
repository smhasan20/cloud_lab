from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# PostgreSQL connection
DATABASE_URL = os.environ.get("DATABASE_URL", "your_render_postgresql_url")
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
            conn.commit()
            return "Registration successful! <a href='/login'>Login</a>"
        except:
            return "Username already exists. <a href='/register'>Try again</a>"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[0], password):
            return f"Welcome, {username}!"
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'Application is running'}, 200

if __name__ == '__main__':
    app.run(debug=True)
