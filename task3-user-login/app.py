from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database connection (similar to first example)
db = psycopg2.connect(
    host='dpg-d0pm1k6uk2gs739qdm50-a',
    user= 'my_db_zt1o_user',
    password='yoNx6WsiUAgIx5XuOO0MjaumivAeiC6Z',
    database='my_db_zt1o',
    port='5432',
    sslmode='require'
)
cursor = db.cursor()

# Initialize database tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(80) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
db.commit()

HTML_STYLE = """
<style>
    body { font-family: Arial, sans-serif; background-color: #f0f2f5; text-align: center; margin-top: 50px; }
    h2 { color: #333; }
    form, .box { display: inline-block; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    input { margin: 10px 0; padding: 8px; width: 90%; border: 1px solid #ccc; border-radius: 4px; }
    input[type="submit"], button { background-color: #007bff; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
    input[type="submit"]:hover, button:hover { background-color: #0056b3; }
    .note { margin-top: 20px; font-size: 14px; color: #555; }
    .flash-message { padding: 10px; margin: 10px 0; border-radius: 4px; }
    .success { background-color: #d4edda; color: #155724; }
    .error { background-color: #f8d7da; color: #721c24; }
</style>
"""

@app.route('/')
def index():
    if 'username' in session:
        return HTML_STYLE + f'''
        <div class="box">
            <h2>Welcome, {session['username']}!</h2>
            <a href="/dashboard"><button>Dashboard</button></a>
            <a href="/logout"><button>Logout</button></a>
        </div>
        '''
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        if not username or not password:
            return HTML_STYLE + '''
            <div class="box">
                <h2>Registration Failed ❌</h2>
                <p class="flash-message error">Username and password are required!</p>
                <a href="/register"><button>Try Again</button></a>
            </div>
            '''
        
        if len(password) < 6:
            return HTML_STYLE + '''
            <div class="box">
                <h2>Registration Failed ❌</h2>
                <p class="flash-message error">Password must be at least 6 characters long!</p>
                <a href="/register"><button>Try Again</button></a>
            </div>
            '''
        
        hashed_pw = generate_password_hash(password)
        
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
            db.commit()
            return HTML_STYLE + '''
            <div class="box">
                <h2>Registration Successful ✅</h2>
                <p class="flash-message success">Please login.</p>
                <a href="/login"><button>Login</button></a>
            </div>
            '''
        except psycopg2.IntegrityError:
            db.rollback()
            return HTML_STYLE + '''
            <div class="box">
                <h2>Registration Failed ❌</h2>
                <p class="flash-message error">Username already exists!</p>
                <a href="/register"><button>Try Again</button></a>
            </div>
            '''
        except Exception as e:
            db.rollback()
            print(f"Registration error: {e}")
            return HTML_STYLE + '''
            <div class="box">
                <h2>Registration Failed ❌</h2>
                <p class="flash-message error">An error occurred. Please try again.</p>
                <a href="/register"><button>Try Again</button></a>
            </div>
            '''
    
    return HTML_STYLE + '''
    <div class="box">
        <h2>Register</h2>
        <form action="/register" method="post">
            <input name="username" placeholder="Username" required><br>
            <input name="password" type="password" placeholder="Password" required><br>
            <input type="submit" value="Register">
        </form>
        <div class="note">
            <p>Already have an account? <a href="/login">Login here</a></p>
        </div>
    </div>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        if not username or not password:
            return HTML_STYLE + '''
            <div class="box">
                <h2>Login Failed ❌</h2>
                <p class="flash-message error">Username and password are required!</p>
                <a href="/login"><button>Try Again</button></a>
            </div>
            '''
        
        try:
            cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('index'))
            else:
                return HTML_STYLE + '''
                <div class="box">
                    <h2>Login Failed ❌</h2>
                    <p class="flash-message error">Invalid username or password!</p>
                    <a href="/login"><button>Try Again</button></a>
                </div>
                '''
        except Exception as e:
            print(f"Login error: {e}")
            return HTML_STYLE + '''
            <div class="box">
                <h2>Login Failed ❌</h2>
                <p class="flash-message error">An error occurred. Please try again.</p>
                <a href="/login"><button>Try Again</button></a>
            </div>
            '''
    
    return HTML_STYLE + '''
    <div class="box">
        <h2>Login</h2>
        <form action="/login" method="post">
            <input name="username" placeholder="Username" required><br>
            <input name="password" type="password" placeholder="Password" required><br>
            <input type="submit" value="Login">
        </form>
        <div class="note">
            <p>Don't have an account? <a href="/register">Register here</a></p>
        </div>
    </div>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return HTML_STYLE + '''
    <div class="box">
        <h2>Logged Out ✅</h2>
        <p class="flash-message success">You have been logged out successfully.</p>
        <a href="/login"><button>Login</button></a>
    </div>
    '''

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return HTML_STYLE + f'''
    <div class="box">
        <h2>Dashboard</h2>
        <p>Welcome, {session['username']}!</p>
        <a href="/"><button>Home</button></a>
        <a href="/logout"><button>Logout</button></a>
    </div>
    '''

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'Application is running'}, 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)