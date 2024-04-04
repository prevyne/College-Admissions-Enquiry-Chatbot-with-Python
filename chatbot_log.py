from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

#Route for the landing page
@app.route('/')
def launch_page():
    # Render the template with conversations data
    return render_template('conversation_logs.html')

#route for conversations page
@app.route('/conversations')
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