from flask import Flask, request, redirect, render_template_string
import psycopg2
from psycopg2 import sql
import hashlib
import os

app = Flask(__name__)

# PostgreSQL connection with error handling
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="dpg-d0pm1k6uk2gs739qdm50-a.oregon-postgres.render.com",  # Full external URL added
            user="my_db_zt1o_user",
            password="yoNx6WsiUAgIx5XuOO0MjaumivAeiC6Z",
            database="my_db_zt1o",
            port=5432,
            sslmode='require'  # SSL mode added
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
    else:
        print("Could not connect to database for initialization")

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Enhanced CSS and HTML templates with modern design
HTML_STYLE = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    
    .container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 400px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    h2 {
        text-align: center;
        color: #333;
        margin-bottom: 30px;
        font-size: 28px;
        font-weight: 600;
    }
    
    .form-group {
        margin-bottom: 20px;
        position: relative;
    }
    
    input[type="text"], input[type="password"] {
        width: 100%;
        padding: 15px 20px;
        border: 2px solid #e1e1e1;
        border-radius: 10px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }
    
    input[type="text"]:focus, input[type="password"]:focus {
        border-color: #667eea;
        outline: none;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    button {
        width: 100%;
        padding: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        font-size: 16px;
        font-weight: 600;
        margin: 15px 0;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    
    .link {
        text-align: center;
        margin-top: 20px;
    }
    
    .link a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .link a:hover {
        color: #764ba2;
    }
    
    .message {
        text-align: center;
        padding: 20px;
        margin: 20px 0;
        border-radius: 15px;
        font-weight: 500;
    }
    
    .success {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #155724;
        border: 2px solid rgba(21, 87, 36, 0.2);
    }
    
    .error {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #721c24;
        border: 2px solid rgba(114, 28, 36, 0.2);
    }
    
    .home-buttons {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    
    .home-buttons a {
        text-decoration: none;
    }
    
    .btn-register {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    }
    
    .btn-login {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    
    .icon {
        font-size: 24px;
        margin-bottom: 10px;
    }
    
    @media (max-width: 480px) {
        .container {
            padding: 30px 20px;
            margin: 10px;
        }
        
        h2 {
            font-size: 24px;
        }
    }
</style>
"""

# Home route
@app.route('/')
def index():
    return render_template_string(HTML_STYLE + '''
    <div class="container">
        <div class="icon">🏠</div>
        <h2>Welcome to Our App</h2>
        <div class="home-buttons">
            <a href="/register">
                <button type="button" class="btn-register">
                    📝 Create New Account
                </button>
            </a>
            <a href="/login">
                <button type="button" class="btn-login">
                    🔐 Login to Account
                </button>
            </a>
        </div>
    </div>
    ''')

# Register page (GET)
@app.route('/register')
def register_page():
    return render_template_string(HTML_STYLE + '''
    <div class="container">
        <div class="icon">📝</div>
        <h2>Create Account</h2>
        <form method="POST" action="/register">
            <div class="form-group">
                <input type="text" name="username" placeholder="Choose a Username" required>
            </div>
            <div class="form-group">
                <input type="password" name="password" placeholder="Create Password" required>
            </div>
            <button type="submit">Register Now</button>
        </form>
        <div class="link">
            <a href="/login">Already have an account? Login here</a>
        </div>
        <div class="link">
            <a href="/">← Back to Home</a>
        </div>
    </div>
    ''')

# Login page (GET)
@app.route('/login')
def login_page():
    return render_template_string(HTML_STYLE + '''
    <div class="container">
        <div class="icon">🔐</div>
        <h2>Welcome Back</h2>
        <form method="POST" action="/login">
            <div class="form-group">
                <input type="text" name="username" placeholder="Enter Username" required>
            </div>
            <div class="form-group">
                <input type="password" name="password" placeholder="Enter Password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <div class="link">
            <a href="/register">Don't have an account? Register here</a>
        </div>
        <div class="link">
            <a href="/">← Back to Home</a>
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
                <div class="icon">❌</div>
                <h3>Registration Failed</h3>
                <p>Please provide both username and password</p>
            </div>
            <div class="link">
                <a href="/register"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')
    
    if len(username) < 3:
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <div class="icon">❌</div>
                <h3>Registration Failed</h3>
                <p>Username must be at least 3 characters long</p>
            </div>
            <div class="link">
                <a href="/register"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')
    
    if len(password) < 6:
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <div class="icon">❌</div>
                <h3>Registration Failed</h3>
                <p>Password must be at least 6 characters long</p>
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
                <div class="icon">🔌</div>
                <h3>Database Connection Error</h3>
                <p>Could not connect to database. Please try again later.</p>
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
                    <div class="icon">👤</div>
                    <h3>Username Already Taken</h3>
                    <p>This username is already registered. Please choose a different one.</p>
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
                <div class="icon">🎉</div>
                <h3>Registration Successful!</h3>
                <p>Welcome <strong>{}</strong>! Your account has been created successfully.</p>
            </div>
            <div class="link">
                <a href="/login"><button type="button">Login Now</button></a>
            </div>
        </div>
        '''.format(username))
        
    except psycopg2.Error as e:
        if conn:
            conn.close()
        print(f"Registration error: {e}")
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <div class="icon">⚠️</div>
                <h3>Registration Failed</h3>
                <p>A database error occurred. Please try again.</p>
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
                <div class="icon">❌</div>
                <h3>Login Failed</h3>
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
                <div class="icon">🔌</div>
                <h3>Database Connection Error</h3>
                <p>Could not connect to database. Please try again later.</p>
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
                    <div class="icon">🎊</div>
                    <h3>Welcome Back!</h3>
                    <p>Hello <strong>{}</strong>! You have successfully logged in.</p>
                </div>
                <div class="link">
                    <a href="/"><button type="button">Go to Dashboard</button></a>
                </div>
            </div>
            '''.format(username))
        else:
            return render_template_string(HTML_STYLE + '''
            <div class="container">
                <div class="message error">
                    <div class="icon">🔒</div>
                    <h3>Login Failed</h3>
                    <p>Invalid username or password. Please check your credentials.</p>
                </div>
                <div class="link">
                    <a href="/login"><button type="button">Try Again</button></a>
                </div>
                <div class="link">
                    <a href="/register">Need an account? Register here</a>
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
                <div class="icon">⚠️</div>
                <h3>Login Failed</h3>
                <p>A database error occurred. Please try again.</p>
            </div>
            <div class="link">
                <a href="/login"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')

# Test database connection route
@app.route('/test-db')
def test_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return f"Database connected successfully! Total users: {count}"
        except Exception as e:
            return f"Database connected but query failed: {e}"
    else:
        return "Database connection failed!"

# Initialize database when app starts
if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)