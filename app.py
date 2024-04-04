from core import *
from update import *
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

import nltk
from nltk.stem import WordNetLemmatizer

#nltk.download('punkt')
#nltk.download('wordnet')

# Initializing the lemmatizer
lemmatizer = WordNetLemmatizer()


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'KabuChat' 

#Routing the update page
@app.route('/update')
def frame_content():
    return render_template('update.html')

# Route to handle saving intents
@app.route('/save', methods=['POST'])
def save():
    intents = load_intents()
    data = request.form.to_dict()
    patterns = [pattern.strip() for pattern in data['patterns'].split(",")]
    responses = [response.strip() for response in data['responses'].split(",")]
    new_intent = {
        "intent": data["intent"],
        "patterns": patterns,
        "responses": responses
    }

# Check if an intent with the same name already exists
    existing_intent = next((intent for intent in intents['intents'] if intent['intent'] == new_intent['intent']), None)
    if existing_intent:
        # Update existing intent
        existing_intent['patterns'].extend(new_intent['patterns'])
        existing_intent['responses'].extend(new_intent['responses'])
    else:
        # Add new intent
        intents['intents'].append(new_intent)
    
    save_intents(intents)
    return jsonify({'success': True})

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
create_users_table() # Creates the "users" table when the application starts

# Route for the home page (registration form)
@app.route("/")
def home():
    return render_template("register.html")

# Route for user registration
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]

    with sqlite3.connect('user_database.db') as conn:
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone() is not None:
            return "Username already exists. Please choose a different username."

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
        return render_template('login.html')

# Route for the user login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform user authentication
        username = request.form['username']
        password = request.form['password']
        
        #check credentials against a database
        if verify_user(username, password):
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Function to verify user credentials
def verify_user(username, password):
    with sqlite3.connect('user_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
    return user is not None


# Route for admin registration
@app.route("/register", methods=["POST"])
def admin_register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]

    with sqlite3.connect('admin_database.db') as conn:
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone() is not None:
            return "Username already exists. Please choose a different username."

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
        return render_template('admin_login.html')


#route for administrator login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
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

# Route for logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Route for the chatbot interface (requires login)
@app.route('/app')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('chat.html')

# Function to determine if user input matches any intent
def find_intent(user_input):
    for intent in intents_data['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_input.lower():
                return intent['intent']
    return None

#chatbot interaction
@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')
    username = session.get('username')  # Retrieves username from session

    # Check if any part of the user input matches any intent
    intent_tag = find_intent(user_input)
    if intent_tag:
        response = str(chatbot.get_response(user_input))
    else:
        response = "I could not recognize your query. Please specify more"

    # Store conversation in the database
    try:
        store_conversation(user_input, response, username)
    except sqlite3.Error:
        return "Error: Unable to store conversation in the database."

    return response

######################################################################
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

#######################################################################
# Function to lemmatize text
def lemmatize_text(text):
    tokens = nltk.word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lemmatized_tokens)

def store_conversation(user_input, bot_response, username):
    conn = sqlite3.connect('chatbot_conversations.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO conversations (user_input, bot_response, timestamp, username) VALUES (?, ?, ?, ?)
    ''', (user_input, bot_response, timestamp, username))
    conn.commit()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)