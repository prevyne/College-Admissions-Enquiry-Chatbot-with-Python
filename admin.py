from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'KabuChat' 

# Function to create the "users" table if it does not exist
def create_users_table():
    with sqlite3.connect('user_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )

        ''')

# Creates the "users" table when the application starts
create_users_table()

"""
# Route for the home page (login form)
@app.route("/")
def home():
    return render_template("admin_login.html")
"""

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform user authentication
        username = request.form['username']
        password = request.form['password']
        
        #check credentials against a database
        if verify_user(username, password):
            session['username'] = username
            return redirect(url_for('display_conversations'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('admin_login.html', error=error)
    return render_template('admin_login.html')

# Function to verify user credentials
def verify_user(username, password):
    with sqlite3.connect('admin_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
    return user is not None

# Route for logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#route for conversations_log page
@app.route('/admin')
def display_conversations():
    # Connect to the SQLite database
    conn = sqlite3.connect('chatbot_conversations.db')
    c = conn.cursor()

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Fetch conversations from the database with pagination
    c.execute("SELECT * FROM conversations LIMIT ? OFFSET ?", (per_page, offset))
    conversations = c.fetchall()

    # Close the database connection
    conn.close()
    return render_template('conversation_logs.html', conversations=conversations)

#route for conversations page
@app.route('/conversations')
def display_all_conversations():
    # Connect to the SQLite database
    conn = sqlite3.connect('chatbot_conversations.db')
    c = conn.cursor()
    
    # Fetch conversations from the database
    c.execute("SELECT * FROM conversations")
    conversations = c.fetchall()
    
    #close database connection
    c = conn.cursor()

    # Render the template with conversations data
    return render_template('conversations.html', conversations=conversations)

#Route for Escalated queries page
@app.route('/escalated')
def display_escalated_queries():
    # Connect to the SQLite database
    conn = sqlite3.connect('chatbot_conversations.db')
    c = conn.cursor()
    
    # Fetch conversations from the database where user input was not recognized
    c.execute("SELECT * FROM conversations where bot_response = 'I could not recognize your query. Please specify more'")
    conversations = c.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Render the template with conversations data
    return render_template('escalated.html', conversations=conversations)

#route for conversations_log page
@app.route('/admin')
def display_conversations():
    # Connect to the SQLite database
    conn = sqlite3.connect('chatbot_conversations.db')
    c = conn.cursor()

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Fetch conversations from the database with pagination
    c.execute("SELECT * FROM conversations LIMIT ? OFFSET ?", (per_page, offset))
    conversations = c.fetchall()

    # Close the database connection
    conn.close()
    return render_template('conversation_logs.html', conversations=conversations)

#route for conversations page
@app.route('/conversations')
def display_all_conversations():
    # Connect to the SQLite database
    conn = sqlite3.connect('chatbot_conversations.db')
    c = conn.cursor()
    
    # Fetch conversations from the database
    c.execute("SELECT * FROM conversations")
    conversations = c.fetchall()
    
    #close database connection
    c = conn.cursor()

    # Render the template with conversations data
    return render_template('conversations.html', conversations=conversations)

#Route for Escalated queries page
@app.route('/escalated')
def display_escalated_queries():
    # Connect to the SQLite database
    conn = sqlite3.connect('chatbot_conversations.db')
    c = conn.cursor()
    
    # Fetch conversations from the database where user input was not recognized
    c.execute("SELECT * FROM conversations where bot_response = 'I could not recognize your query. Please specify more'")
    conversations = c.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Render the template with conversations data
    return render_template('escalated.html', conversations=conversations)
if __name__ == '__main__':
    app.run(debug=True)
