from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

#Displaying i-frame content
app = Flask(__name__, template_folder='templates')

@app.route('/')
def frame_content():
    # Reading the update.html page
    with open('update.html', 'r') as f:
        content = f.read()
    return content

if __name__ == '__main__':
    app.run(debug=True)