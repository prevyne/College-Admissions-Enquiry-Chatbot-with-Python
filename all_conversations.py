from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def display_conversations():
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

if __name__ == '__main__':
    app.run(debug=True)