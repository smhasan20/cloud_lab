from flask import Flask, request, redirect, render_template_string, session, flash
import psycopg2
from psycopg2 import sql
import hashlib
import os
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# PostgreSQL connection with better error handling
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="dpg-d0pm1k6uk2gs739qdm50-a.oregon-postgres.render.com",
            user="my_db_zt1o_user", 
            password="yoNx6WsiUAgIx5XuOO0MjaumivAeiC6Z",
            database="my_db_zt1o",
            port=5432,
            sslmode='require',
            connect_timeout=10
        )
        logger.info("Database connection successful")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

# Initialize database with retry logic
def init_db():
    max_retries = 3
    for attempt in range(max_retries):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE,
                        full_name VARCHAR(100),
                        phone VARCHAR(20),
                        password VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
                cursor.close()
                conn.close()
                logger.info("Database initialized successfully")
                return True
            except psycopg2.Error as e:
                logger.error(f"Database initialization error: {e}")
                if conn:
                    conn.close()
        
        logger.warning(f"Database initialization attempt {attempt + 1} failed")
        if attempt < max_retries - 1:
            import time
            time.sleep(2)
    
    logger.error("Could not initialize database after multiple attempts")
    return False

# Enhanced password hashing
def hash_password(password):
    salt = "your_salt_here"  # Production এ unique salt use করবেন
    return hashlib.sha256((password + salt).encode()).hexdigest()

# Modern CSS with glassmorphism and animations
HTML_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }
    
    body::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(120, 219, 255, 0.3) 0%, transparent 50%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(1deg); }
    }
    
    .container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 40px;
        border-radius: 24px;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        width: 100%;
        max-width: 420px;
        position: relative;
        z-index: 10;
        animation: slideUp 0.6s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 24px;
        z-index: -1;
    }
    
    .icon {
        font-size: 48px;
        text-align: center;
        margin-bottom: 20px;
        animation: bounce 2s infinite;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    h2 {
        text-align: center;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 30px;
        font-size: 32px;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        letter-spacing: -0.5px;
    }
    
    .form-group {
        margin-bottom: 24px;
        position: relative;
    }
    
    .input-wrapper {
        position: relative;
        overflow: hidden;
        border-radius: 16px;
    }
    
    input[type="text"], input[type="password"], input[type="email"] {
        width: 100%;
        padding: 18px 24px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        font-size: 16px;
        font-weight: 400;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Inter', sans-serif;
    }
    
    input::placeholder {
        color: rgba(255, 255, 255, 0.6);
        font-weight: 400;
    }
    
    input[type="text"]:focus, input[type="password"]:focus, input[type="email"]:focus {
        border-color: rgba(255, 255, 255, 0.4);
        outline: none;
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 
            0 0 0 4px rgba(255, 255, 255, 0.1),
            0 8px 32px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    button {
        width: 100%;
        padding: 18px 24px;
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
        color: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        cursor: pointer;
        font-size: 16px;
        font-weight: 600;
        margin: 12px 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: none;
        letter-spacing: 0.5px;
        font-family: 'Inter', sans-serif;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    button:hover::before {
        left: 100%;
    }
    
    button:hover {
        transform: translateY(-3px);
        box-shadow: 
            0 12px 24px rgba(0, 0, 0, 0.15),
            0 0 0 1px rgba(255, 255, 255, 0.1);
        background: linear-gradient(135deg, rgba(255,255,255,0.25) 0%, rgba(255,255,255,0.15) 100%);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    button:active {
        transform: translateY(-1px);
    }
    
    .link {
        text-align: center;
        margin-top: 24px;
    }
    
    .link a {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        font-size: 14px;
        border-bottom: 1px solid transparent;
    }
    
    .link a:hover {
        color: rgba(255, 255, 255, 0.95);
        border-bottom-color: rgba(255, 255, 255, 0.5);
    }
    
    .message {
        text-align: center;
        padding: 24px;
        margin: 24px 0;
        border-radius: 20px;
        font-weight: 500;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .success {
        background: linear-gradient(135deg, rgba(132, 250, 176, 0.2) 0%, rgba(143, 211, 244, 0.2) 100%);
        color: rgba(255, 255, 255, 0.95);
        border-color: rgba(132, 250, 176, 0.3);
    }
    
    .error {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(255, 142, 83, 0.2) 100%);
        color: rgba(255, 255, 255, 0.95);
        border-color: rgba(255, 107, 107, 0.3);
    }
    
    .home-buttons {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    
    .home-buttons a {
        text-decoration: none;
    }
    
    .btn-register {
        background: linear-gradient(135deg, rgba(132, 250, 176, 0.2) 0%, rgba(143, 211, 244, 0.2) 100%);
        border-color: rgba(132, 250, 176, 0.3);
    }
    
    .btn-login {
        background: linear-gradient(135deg, rgba(168, 237, 234, 0.2) 0%, rgba(254, 214, 227, 0.2) 100%);
        border-color: rgba(168, 237, 234, 0.3);
    }
    
    .stats {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }
    
    .stat-item {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
    }
    
    .stat-number {
        font-size: 24px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.95);
    }
    
    .floating-shapes {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 1;
        pointer-events: none;
    }
    
    .shape {
        position: absolute;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: floatUp 8s infinite linear;
    }
    
    .shape:nth-child(1) {
        width: 80px;
        height: 80px;
        left: 10%;
        animation-delay: 0s;
    }
    
    .shape:nth-child(2) {
        width: 120px;
        height: 120px;
        left: 20%;
        animation-delay: 2s;
    }
    
    .shape:nth-child(3) {
        width: 60px;
        height: 60px;
        left: 70%;
        animation-delay: 4s;
    }
    
    @keyframes floatUp {
        0% {
            bottom: -150px;
            transform: translateX(0px) rotate(0deg);
            opacity: 1;
        }
        100% {
            bottom: 100vh;
            transform: translateX(-100px) rotate(180deg);
            opacity: 0;
        }
    }
    
    @media (max-width: 480px) {
        .container {
            padding: 32px 24px;
            margin: 16px;
            border-radius: 20px;
        }
        
        h2 {
            font-size: 28px;
            margin-bottom: 24px;
        }
        
        .icon {
            font-size: 40px;
        }
        
        input[type="text"], input[type="password"], input[type="email"] {
            padding: 16px 20px;
            font-size: 16px;
        }
        
        button {
            padding: 16px 20px;
            font-size: 16px;
        }
    }
    
    .loader {
        display: none;
        width: 20px;
        height: 20px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: rgba(255, 255, 255, 0.8);
        animation: spin 1s ease-in-out infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .form-loading .loader {
        display: block;
    }
    
    .form-loading button {
        opacity: 0.7;
        pointer-events: none;
    }
</style>
"""

# Home route with floating shapes
@app.route('/')
def index():
    return render_template_string(HTML_STYLE + '''
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    <div class="container">
        <div class="icon">🚀</div>
        <h2>Welcome Back</h2>
        <p style="text-align: center; color: rgba(255,255,255,0.8); margin-bottom: 30px; font-weight: 400;">
            Manage your account with style
        </p>
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">🔐</div>
                <div>Secure</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">⚡</div>
                <div>Fast</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">🎯</div>
                <div>Simple</div>
            </div>
        </div>
        <div class="home-buttons">
            <a href="/register">
                <button type="button" class="btn-register">
                    📝 Create New Account
                </button>
            </a>
            <a href="/login">
                <button type="button" class="btn-login">
                    🔑 Login to Account
                </button>
            </a>
        </div>
    </div>
    ''')

# Enhanced Register page with validation
@app.route('/register')
def register_page():
    return render_template_string(HTML_STYLE + '''
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    <div class="container">
        <div class="icon">✨</div>
        <h2>Create Account</h2>
        <form method="POST" action="/register" id="registerForm">
            <div class="form-group">
                <div class="input-wrapper">
                    <input type="text" name="username" placeholder="Username (min 3 chars)" required minlength="3">
                </div>
            </div>
            <div class="form-group">
                <div class="input-wrapper">
                    <input type="email" name="email" placeholder="Email (optional)">
                </div>
            </div>
            <div class="form-group">
                <div class="input-wrapper">
                    <input type="password" name="password" placeholder="Password (min 6 chars)" required minlength="6">
                </div>
            </div>
            <div class="loader"></div>
            <button type="submit">Create Account</button>
        </form>
        <div class="link">
            <a href="/login">Already have an account? Login here</a>
        </div>
        <div class="link">
            <a href="/">← Back to Home</a>
        </div>
    </div>
    
    <script>
        document.getElementById('registerForm').addEventListener('submit', function() {
            this.classList.add('form-loading');
        });
    </script>
    ''')

# Enhanced Login page
@app.route('/login')
def login_page():
    return render_template_string(HTML_STYLE + '''
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    <div class="container">
        <div class="icon">🔮</div>
        <h2>Welcome Back</h2>
        <form method="POST" action="/login" id="loginForm">
            <div class="form-group">
                <div class="input-wrapper">
                    <input type="text" name="username" placeholder="Enter Username" required>
                </div>
            </div>
            <div class="form-group">
                <div class="input-wrapper">
                    <input type="password" name="password" placeholder="Enter Password" required>
                </div>
            </div>
            <div class="loader"></div>
            <button type="submit">Login</button>
        </form>
        <div class="link">
            <a href="/register">Need an account? Register here</a>
        </div>
        <div class="link">
            <a href="/">← Back to Home</a>
        </div>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', function() {
            this.classList.add('form-loading');
        });
    </script>
    ''')

# Enhanced Register POST with better validation
@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Input validation
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
                    <div class="icon">⚠️</div>
                    <h3>Username Too Short</h3>
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
                    <div class="icon">🔒</div>
                    <h3>Password Too Short</h3>
                    <p>Password must be at least 6 characters long</p>
                </div>
                <div class="link">
                    <a href="/register"><button type="button">Try Again</button></a>
                </div>
            </div>
            ''')
        
        # Database operations with retry
        max_retries = 3
        for attempt in range(max_retries):
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    
                    # Check if username exists
                    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
                    if cursor.fetchone():
                        cursor.close()
                        conn.close()
                        return render_template_string(HTML_STYLE + '''
                        <div class="container">
                            <div class="message error">
                                <div class="icon">👤</div>
                                <h3>Username Already Exists</h3>
                                <p>This username is already registered. Please choose another one.</p>
                            </div>
                            <div class="link">
                                <a href="/register"><button type="button">Try Again</button></a>
                            </div>
                        </div>
                        ''')
                    
                    # Insert new user
                    hashed_password = hash_password(password)
                    if email:
                        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                                      (username, email, hashed_password))
                    else:
                        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                                      (username, hashed_password))
                    
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    logger.info(f"User {username} registered successfully")
                    
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
                        <div class="link">
                            <a href="/">Go to Home</a>
                        </div>
                    </div>
                    '''.format(username))
                    
                except psycopg2.Error as e:
                    logger.error(f"Database error during registration: {e}")
                    if conn:
                        conn.close()
                    
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(1)
                        continue
                    else:
                        break
            else:
                if attempt < max_retries - 1:
                    import time
                    time.sleep(1)
                    continue
                else:
                    break
        
        # If we reach here, all attempts failed
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <div class="icon">🔌</div>
                <h3>Database Connection Error</h3>
                <p>Sorry, we cannot connect to the database right now. Please try again later.</p>
            </div>
            <div class="link">
                <a href="/register"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')
        
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <div class="icon">⚠️</div>
                <h3>Registration Failed</h3>
                <p>An unexpected error occurred. Please try again later.</p>
            </div>
            <div class="link">
                <a href="/register"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')

# Enhanced Login POST with better validation  
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Input validation
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
        
        # Database operations with retry
        max_retries = 3
        for attempt in range(max_retries):
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    hashed_password = hash_password(password)
                    cursor.execute("SELECT username FROM users WHERE username = %s AND password = %s", 
                                  (username, hashed_password))
                    user = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    
                    if user:
                        logger.info(f"User {username} logged in successfully")
                        session['username'] = username
                        return render_template_string(HTML_STYLE + '''
                        <div class="container">
                            <div class="message success">
                                <div class="icon">🎊</div>
                                <h3>Welcome Back!</h3>
                                <p>Hello <strong>{}</strong>! You have successfully logged in.</p>
                            </div>
                            <div class="link">
                                <a href="/dashboard"><button type="button">Go to Dashboard</button></a>
                            </div>
                            <div class="link">
                                <a href="/">Go to Home</a>
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
                    logger.error(f"Database error during login: {e}")
                    if conn:
                        conn.close()
                    
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(1)
                        continue
                    else:
                        break
            else:
                if attempt < max_retries - 1:
                    import time
                    time.sleep(1)
                    continue
                else:
                    break
        
        # If we reach here, all attempts failed
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
        
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <div class="icon">⚠️</div>
                <h3>Login Failed</h3>
                <p>An unexpected error occurred. Please try again later.</p>
            </div>
            <div class="link">
                <a href="/login"><button type="button">Try Again</button></a>
            </div>
        </div>
        ''')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    
    username = session['username']
    return render_template_string(HTML_STYLE + '''
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    <div class="container">
        <div class="icon">🎯</div>
        <h2>Dashboard</h2>
        <div class="message success">
            <div class="icon">👋</div>
            <h3>Welcome, {}!</h3>
            <p>You are successfully logged in to your dashboard.</p>
        </div>
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">✅</div>
                <div>Active</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">🔐</div>
                <div>Secure</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">🚀</div>
                <div>Ready</div>
            </div>
        </div>
        <div class="home-buttons">
            <a href="/logout">
                <button type="button" style="background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(255, 142, 83, 0.2) 100%); border-color: rgba(255, 107, 107, 0.3);">
                    🚪 Logout
                </button>
            </a>
            <a href="/">
                <button type="button">
                    🏠 Home
                </button>
            </a>
        </div>
    </div>
    '''.format(username))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template_string(HTML_STYLE + '''
    <div class="container">
        <div class="message success">
            <div class="icon">👋</div>
            <h3>Logged Out Successfully</h3>
            <p>You have been safely logged out. See you again!</p>
        </div>
        <div class="link">
            <a href="/login"><button type="button">Login Again</button></a>
        </div>
        <div class="link">
            <a href="/">Go to Home</a>
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
            return render_template_string(HTML_STYLE + '''
            <div class="container">
                <div class="message success">
                    <div class="icon">✅</div>
                    <h3>Database Connected!</h3>
                    <p>Connection successful. Total users: <strong>{}</strong></p>
                </div>
                <div class="link">
                    <a href="/"><button type="button">Go Home</button></a>
                </div>
            </div>
            '''.format(count))
        except Exception as e:
            return render_template_string(HTML_STYLE + '''
            <div class="container">
                <div class="message error">
                    <div class="icon">⚠️</div>
                    <h3>Database Query Failed</h3>
                    <p>Connected but query failed: {}</p>
                </div>
                <div class="link">
                    <a href="/"><button type="button">Go Home</button></a>
                </div>
            </div>
            '''.format(str(e)))
    else:
        return render_template_string(HTML_STYLE + '''
        <div class="container">
            <div class="message error">
                <div class="icon">❌</div>
                <h3>Database Connection Failed</h3>
                <p>Could not connect to the database.</p>
            </div>
            <div class="link">
                <a href="/"><button type="button">Go Home</button></a>
            </div>
        </div>
        ''')

# Initialize database when app starts
if __name__ == '__main__':
    print("Initializing database...")
    if init_db():
        print("Database initialized successfully")
    else:
        print("Database initialization failed")
    
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)