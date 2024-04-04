from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/update')
def frame_content():
    return render_template('update.html')


@app.route('/')
def display_conversations():
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