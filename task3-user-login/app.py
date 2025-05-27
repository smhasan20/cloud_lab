from flask import Flask, request, redirect, render_template_string
import psycopg2
from psycopg2 import sql
import hashlib

app = Flask(__name__)

# PostgreSQL connection with error handling
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="dpg-d0pm1k6uk2gs739qdm50-a",
            user="my_db_zt1o_user",
            password="yoNx6WsiUAgIx5XuOO0MjaumivAeiC6Z",
            database="my_db_zt1o",
            port=5432
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

# Initialize database
def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print("Database initialized successfully")
        except psycopg2.Error as e:
            print(f"Database initialization error: {e}")

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# CSS and HTML templates
HTML_STYLE = """
<style>
    body {
        font-family: Arial, sans-serif;
        max-width: 400px;
        margin: 50px auto;
        padding: 20px;
        background-color: #f5f5f5;
    }
    .container {
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h2 {
        text-align: center;
        color: #333;
        margin-bottom: 30px;
    }
    input[type="text"], input[type="password"] {
        width: 100%;
        padding: 12px;
        margin: 10px 0;
        border: 1px solid #ddd;
        border-radius: 5px;
        box-sizing: border-box;
    }
    button {
        width: 100%;
        padding: 12px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        margin: 10px 0;
    }
    button:hover {
        background-color: #0056b3;
    }
    .link {
        text-align: center;
        margin-top: 20px;
    }
    .link a {
        color: #007bff;
        text-decoration: none;
    }
    .message {
        text-align: center;
        padding: 20px;
        margin: 20px 0;
        border-radius: 5px;
    }
    .success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
"""

# Home route
@app.route('/')
def index():
    return render_template_string(HTML_STYLE + '''
    <div class="container">
        <h2>Welcome</h2>
        <div style="text-align: center;">
            <a href="/register"><button type="button">Register</button></a>
            <a href="/login"><button type="button">Login</button></a>
        </div>
    </div>
    ''')

# Register page (GET)
@app.route('/register')
def register_page():
    return render_template_string(HTML_STYLE + '''
    <div class="container">
        <h2>Register</h2>
        <form method="POST" action="/register">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
        <div class="link">
            <a href="/login">Already have an account? Login here</a>
        </div>
        <div class="link">
            <a href="/">Back to Home</a>
        </div>
    </div>
    ''')

# Login page (GET)
@app.route('/login')
def login_page():
    return render_template_string(HTML_STYLE + '''
    <div class="container">
        <h2>Login</h2>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="link">
            <a href="/register">Don't have an account? Register here</a>
        </div>
        <div class="link">
            <a href="/">Back to Home</a>
        </div>
    </div>
    ''')

# Register (POST)
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <h3>Registration Failed ❌</h3>
                <p>Please provide both username and password</p>
            </div>
            <div class="link">
                <a href="/register"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')
    
    conn = get_db_connection()
    if not conn:
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <h3>Database Error ❌</h3>
                <p>Could not connect to database</p>
            </div>
            <div class="link">
                <a href="/register"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')
    
    try:
        cursor = conn.cursor()
        # Check if username already exists
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return render_template_string(HTML_STYLE + '''
            <div class="container">
                <div class="message error">
                    <h3>Registration Failed ❌</h3>
                    <p>Username already exists. Please choose a different username.</p>
                </div>
                <div class="link">
                    <a href="/register"><button type="button">Try Again</button></a>
                </div>
            </div>
            ''')
        
        # Insert new user
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                      (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message success">
                <h3>Registration Successful ✅</h3>
                <p>Your account has been created successfully!</p>
            </div>
            <div class="link">
                <a href="/login"><button type="button">Login Now</button></a>
            </div>
        </div>
        ''')
        
    except psycopg2.Error as e:
        if conn:
            conn.close()
        print(f"Registration error: {e}")
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <h3>Registration Failed ❌</h3>
                <p>Database error occurred. Please try again.</p>
            </div>
            <div class="link">
                <a href="/register"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')

# Login (POST)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <h3>Login Failed ❌</h3>
                <p>Please provide both username and password</p>
            </div>
            <div class="link">
                <a href="/login"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')
    
    conn = get_db_connection()
    if not conn:
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <h3>Database Error ❌</h3>
                <p>Could not connect to database</p>
            </div>
            <div class="link">
                <a href="/login"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')
    
    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute("SELECT username FROM users WHERE username = %s AND password = %s", 
                      (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return render_template_string(HTML_STYLE + '''
            <div class="container">
                <div class="message success">
                    <h3>Login Successful ✅</h3>
                    <p>Welcome back, {}!</p>
                </div>
                <div class="link">
                    <a href="/"><button type="button">Go to Home</button></a>
                </div>
            </div>
            '''.format(username))
        else:
            return render_template_string(HTML_STYLE + '''
            <div class="container">
                <div class="message error">
                    <h3>Login Failed ❌</h3>
                    <p>Invalid username or password</p>
                </div>
                <div class="link">
                    <a href="/login"><button type="button">Try Again</button></a>
                </div>
            </div>
            ''')
            
    except psycopg2.Error as e:
        if conn:
            conn.close()
        print(f"Login error: {e}")
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <h3>Login Failed ❌</h3>
                <p>Database error occurred. Please try again.</p>
            </div>
            <div class="link">
                <a href="/login"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')

# Initialize database when app starts
init_db()

# Run the app
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)