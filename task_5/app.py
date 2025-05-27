from flask import Flask, request, render_template_string, session, redirect, url_for
import psycopg2
import hashlib
import os
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-2025'


def get_db_connection():
      try:
        conn = psycopg2.connect(
            host="dpg-d0pm1k6uk2gs739qdm50-a.oregon-postgres.render.com",  # Full external URL
            user="my_db_zt1o_user",
            password="yoNx6WsiUAgIx5XuOO0MjaumivAeiC6Z",
            database="my_db_zt1o",
            port=5432,
            sslmode='require'  # SSL mode যোগ করা হলো
        )
        return conn
      except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

# Initialize database tables
def init_database():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Create users table with validation fields
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20),
                    is_verified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    login_attempts INTEGER DEFAULT 0,
                    account_status VARCHAR(20) DEFAULT 'active'
                );
            """)
            
            # Create user sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    session_token VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                );
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            print("Database initialized successfully")
        except psycopg2.Error as e:
            print(f"Database initialization error: {e}")

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Phone validation
def is_valid_phone(phone):
    pattern = r'^[\+]?[1-9]?[0-9]{7,15}$'
    return re.match(pattern, phone) is not None

# CSS Styles
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
    }
    .container {
        background: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 450px;
        margin: 20px;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
    }
    .header h2 {
        color: #333;
        font-size: 28px;
        margin-bottom: 10px;
    }
    .header p {
        color: #666;
        font-size: 14px;
    }
    .form-group {
        margin-bottom: 20px;
    }
    .form-group label {
        display: block;
        margin-bottom: 8px;
        color: #333;
        font-weight: 500;
    }
    .form-group input {
        width: 100%;
        padding: 12px 15px;
        border: 2px solid #e1e1e1;
        border-radius: 8px;
        font-size: 16px;
        transition: border-color 0.3s;
    }
    .form-group input:focus {
        outline: none;
        border-color: #667eea;
    }
    .btn {
        width: 100%;
        padding: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .btn:hover {
        transform: translateY(-2px);
    }
    .links {
        text-align: center;
        margin-top: 20px;
    }
    .links a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }
    .links a:hover {
        text-decoration: underline;
    }
    .message {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
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
    .warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    .dashboard {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 600px;
        margin: 20px;
    }
    .user-info {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .user-info h3 {
        color: #333;
        margin-bottom: 15px;
    }
    .info-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e1e1e1;
    }
    .info-item:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    .info-label {
        font-weight: 500;
        color: #666;
    }
    .info-value {
        color: #333;
    }
    .status-active {
        color: #28a745;
        font-weight: bold;
    }
    .status-inactive {
        color: #dc3545;
        font-weight: bold;
    }
</style>
"""

# Home route
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    return render_template_string(HTML_STYLE + '''
    <div class="container">
        <div class="header">
            <h2>🔐 User Validation System</h2>
            <p>Secure Authentication with PostgreSQL</p>
        </div>
        <div style="text-align: center;">
            <a href="/register" style="text-decoration: none;">
                <button class="btn" style="margin-bottom: 10px;">Create Account</button>
            </a>
            <br>
            <a href="/login" style="text-decoration: none;">
                <button class="btn">Login to Account</button>
            </a>
        </div>
        <div class="links">
            <a href="/admin">Admin Panel</a>
        </div>
    </div>
    ''')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        
        if not email or not is_valid_email(email):
            errors.append("Please enter a valid email address")
        
        if not password or len(password) < 6:
            errors.append("Password must be at least 6 characters long")
        
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        if not full_name or len(full_name) < 2:
            errors.append("Please enter your full name")
        
        if phone and not is_valid_phone(phone):
            errors.append("Please enter a valid phone number")
        
        if errors:
            error_msg = "<br>".join(errors)
            return render_template_string(HTML_STYLE + f'''
            <div class="container">
                <div class="message error">
                    <h3>Registration Failed ❌</h3>
                    <p>{error_msg}</p>
                </div>
                <div class="links">
                    <a href="/register">Try Again</a> | <a href="/">Home</a>
                </div>
            </div>
            ''')
        
        # Database operations
        conn = get_db_connection()
        if not conn:
            return render_template_string(HTML_STYLE + '''
            <div class="container">
                <div class="message error">
                    <h3>Database Error ❌</h3>
                    <p>Could not connect to database. Please try again later.</p>
                </div>
                <div class="links">
                    <a href="/register">Try Again</a>
                </div>
            </div>
            ''')
        
        try:
            cursor = conn.cursor()
            
            # Check if username or email already exists
            cursor.execute("SELECT username, email FROM users WHERE username = %s OR email = %s", 
                          (username, email))
            existing_user = cursor.fetchone()
            
            if existing_user:
                cursor.close()
                conn.close()
                return render_template_string(HTML_STYLE + '''
                <div class="container">
                    <div class="message error">
                        <h3>Registration Failed ❌</h3>
                        <p>Username or email already exists. Please choose different credentials.</p>
                    </div>
                    <div class="links">
                        <a href="/register">Try Again</a>
                    </div>
                </div>
                ''')
            
            # Insert new user
            hashed_password = hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, email, password, full_name, phone, is_verified, account_status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (username, email, hashed_password, full_name, phone, True, 'active'))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return render_template_string(HTML_STYLE + f'''
            <div class="container">
                <div class="message success">
                    <h3>Registration Successful ✅</h3>
                    <p>Welcome {full_name}! Your account has been created successfully.</p>
                    <p>Username: <strong>{username}</strong></p>
                    <p>Email: <strong>{email}</strong></p>
                </div>
                <div class="links">
                    <a href="/login">Login Now</a> | <a href="/">Home</a>
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
                <div class="links">
                    <a href="/register">Try Again</a>
                </div>
            </div>
            ''')
    
    # GET request - show registration form
    return render_template_string(HTML_STYLE + '''
    <div class="container">
        <div class="header">
            <h2>📝 Create Account</h2>
            <p>Join our secure platform</p>
        </div>
        <form method="POST">
            <div class="form-group">
                <label>Username *</label>
                <input type="text" name="username" required maxlength="50">
            </div>
            <div class="form-group">
                <label>Email Address *</label>
                <input type="email" name="email" required maxlength="100">
            </div>
            <div class="form-group">
                <label>Full Name *</label>
                <input type="text" name="full_name" required maxlength="100">
            </div>
            <div class="form-group">
                <label>Phone Number</label>
                <input type="tel" name="phone" maxlength="20" placeholder="+8801XXXXXXXXX">
            </div>
            <div class="form-group">
                <label>Password *</label>
                <input type="password" name="password" required minlength="6">
            </div>
            <div class="form-group">
                <label>Confirm Password *</label>
                <input type="password" name="confirm_password" required minlength="6">
            </div>
            <button type="submit" class="btn">Create Account</button>
        </form>
        <div class="links">
            <a href="/login">Already have an account? Login</a><br>
            <a href="/">← Back to Home</a>
        </div>
    </div>
    ''')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')
        
        if not username_or_email or not password:
            return render_template_string(HTML_STYLE + '''
            <div class="container">
                <div class="message error">
                    <h3>Login Failed ❌</h3>
                    <p>Please provide both username/email and password</p>
                </div>
                <div class="links">
                    <a href="/login">Try Again</a>
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
                <div class="links">
                    <a href="/login">Try Again</a>
                </div>
            </div>
            ''')
        
        try:
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            
            # Check user credentials
            cursor.execute("""
                SELECT id, username, email, full_name, account_status, login_attempts 
                FROM users 
                WHERE (username = %s OR email = %s) AND password = %s
            """, (username_or_email, username_or_email.lower(), hashed_password))
            
            user = cursor.fetchone()
            
            if user:
                user_id, username, email, full_name, account_status, login_attempts = user
                
                if account_status != 'active':
                    cursor.close()
                    conn.close()
                    return render_template_string(HTML_STYLE + '''
                    <div class="container">
                        <div class="message warning">
                            <h3>Account Suspended ⚠️</h3>
                            <p>Your account has been suspended. Please contact administrator.</p>
                        </div>
                        <div class="links">
                            <a href="/">Home</a>
                        </div>
                    </div>
                    ''')
                
                # Update login info
                cursor.execute("""
                    UPDATE users 
                    SET last_login = %s, login_attempts = 0 
                    WHERE id = %s
                """, (datetime.now(), user_id))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                # Set session
                session['user_id'] = user_id
                session['username'] = username
                session['full_name'] = full_name
                
                return redirect(url_for('dashboard'))
            
            else:
                # Failed login - increment attempts
                cursor.execute("""
                    UPDATE users 
                    SET login_attempts = login_attempts + 1 
                    WHERE username = %s OR email = %s
                """, (username_or_email, username_or_email.lower()))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                return render_template_string(HTML_STYLE + '''
                <div class="container">
                    <div class="message error">
                        <h3>Login Failed ❌</h3>
                        <p>Invalid username/email or password</p>
                    </div>
                    <div class="links">
                        <a href="/login">Try Again</a> | <a href="/register">Create Account</a>
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
                <div class="links">
                    <a href="/login">Try Again</a>
                </div>
            </div>
            ''')
    
    # GET request - show login form
    return render_template_string(HTML_STYLE + '''
    <div class="container">
        <div class="header">
            <h2>🔑 Login</h2>
            <p>Access your secure account</p>
        </div>
        <form method="POST">
            <div class="form-group">
                <label>Username or Email</label>
                <input type="text" name="username_or_email" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn">Login</button>
        </form>
        <div class="links">
            <a href="/register">Don't have an account? Register</a><br>
            <a href="/">← Back to Home</a>
        </div>
    </div>
    ''')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        return "Database connection error"
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, email, full_name, phone, is_verified, 
                   created_at, last_login, login_attempts, account_status
            FROM users WHERE id = %s
        """, (session['user_id'],))
        
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user_data:
            username, email, full_name, phone, is_verified, created_at, last_login, login_attempts, account_status = user_data
            
            return render_template_string(HTML_STYLE + f'''
            <div class="dashboard">
                <div class="header">
                    <h2>👤 User Dashboard</h2>
                    <p>Welcome back, {full_name}!</p>
                </div>
                
                <div class="user-info">
                    <h3>Account Information</h3>
                    <div class="info-item">
                        <span class="info-label">Username:</span>
                        <span class="info-value">{username}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Full Name:</span>
                        <span class="info-value">{full_name}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Email:</span>
                        <span class="info-value">{email}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Phone:</span>
                        <span class="info-value">{phone if phone else 'Not provided'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Account Status:</span>
                        <span class="info-value status-{'active' if account_status == 'active' else 'inactive'}">
                            {account_status.upper()}
                        </span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Verified:</span>
                        <span class="info-value">{'✅ Yes' if is_verified else '❌ No'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Member Since:</span>
                        <span class="info-value">{created_at.strftime('%B %d, %Y') if created_at else 'Unknown'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Last Login:</span>
                        <span class="info-value">{last_login.strftime('%B %d, %Y at %I:%M %p') if last_login else 'Never'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Login Attempts:</span>
                        <span class="info-value">{login_attempts}</span>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <a href="/logout" style="text-decoration: none;">
                        <button class="btn">Logout</button>
                    </a>
                </div>
            </div>
            ''')
        
    except psycopg2.Error as e:
        print(f"Dashboard error: {e}")
        return "Error loading dashboard"

# Admin panel
@app.route('/admin')
def admin():
    conn = get_db_connection()
    if not conn:
        return "Database connection error"
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as total_users,
                   COUNT(CASE WHEN account_status = 'active' THEN 1 END) as active_users,
                   COUNT(CASE WHEN is_verified = true THEN 1 END) as verified_users
            FROM users
        """)
        stats = cursor.fetchone()
        
        cursor.execute("""
            SELECT username, email, full_name, account_status, 
                   created_at, last_login
            FROM users 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        recent_users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        total_users, active_users, verified_users = stats
        
        users_html = ""
        for user in recent_users:
            username, email, full_name, status, created_at, last_login = user
            users_html += f"""
            <div class="info-item">
                <div>
                    <strong>{full_name}</strong> (@{username})<br>
                    <small>{email}</small>
                </div>
                <div style="text-align: right;">
                    <span class="status-{'active' if status == 'active' else 'inactive'}">{status}</span><br>
                    <small>{created_at.strftime('%m/%d/%Y') if created_at else 'Unknown'}</small>
                </div>
            </div>
            """
        
        return render_template_string(HTML_STYLE + f'''
        <div class="dashboard">
            <div class="header">
                <h2>⚙️ Admin Panel</h2>
                <p>System Overview</p>
            </div>
            
            <div class="user-info">
                <h3>📊 Statistics</h3>
                <div class="info-item">
                    <span class="info-label">Total Users:</span>
                    <span class="info-value">{total_users}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Active Users:</span>
                    <span class="info-value status-active">{active_users}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Verified Users:</span>
                    <span class="info-value">{verified_users}</span>
                </div>
            </div>
            
            <div class="user-info">
                <h3>👥 Recent Users</h3>
                {users_html}
            </div>
            
            <div style="text-align: center;">
                <a href="/" style="text-decoration: none;">
                    <button class="btn">Back to Home</button>
                </a>
            </div>
        </div>
        ''')
        
    except psycopg2.Error as e:
        print(f"Admin panel error: {e}")
        return "Error loading admin panel"

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Initialize database on startup
init_database()

# Run the application
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)