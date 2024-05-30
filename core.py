import json
import sqlite3
from chatterbot import ChatBot
from datetime import datetime
import time


# Creating an object of ChatBot class with Storage Adapter
chatbot = ChatBot(
    'MyChatbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapter=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Sorry, I am unable to process your request. Please try again, or contact us for help.',
            'maximum_similarity_threshold': 0.10
        }
    ],
    preprocessors=[
        'chatterbot.preprocessors.convert_to_ascii', 
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.clean_whitespace'
    ]
)

# Loading intents from JSON file
try:
    with open('intents.json', 'r', encoding='utf-8') as file:
        intents_data = json.load(file)
except FileNotFoundError:
    print("Error: File 'intents.json' not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: Unable to parse JSON file.")
    exit(1)


# Connect to SQLite database
conn = sqlite3.connect('chatbot_conversations.db')
cursor = conn.cursor()

# Create conversations table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY,
        user_input TEXT,
        bot_response TEXT,
        timestamp TEXT,
        username TEXT
    )
''')

# Commit changes and close database connection
conn.commit()


# Function to insert conversation into database
def insert_conversation(user_input, bot_response, username):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO conversations (user_input, bot_response, timestamp, username) VALUES (?, ?, ?, ?)',
                   (user_input, bot_response, timestamp, username))
    conn.commit()


# Function to print response letter by letter
def print_response_letter_by_letter(response):
    response_text = str(response)
    for letter in response_text:
        print(letter, end='', flush=True)  # Print the letter without newlines and flush the output
        time.sleep(0.1)  # Introduce a delay of 0.1 seconds between printing each letter
    print()  # Print a newline after printing the complete response

# Close database connection
conn.close()