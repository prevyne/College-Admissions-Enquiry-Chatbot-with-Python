from core import *
import json
import sqlite3
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from datetime import datetime
import time

# Creating a new ListTrainer
trainer = ListTrainer(chatbot)
#trainer = ChatterBotCorpusTrainer(chatbot)
#trainer.train('chatterbot.corpus.english')

# Train the chatbot using intents data
for intent_data in intents_data.get("intents", []):
    # Check if 'patterns' and 'responses' keys are present
    patterns = intent_data.get("patterns", [])
    responses = intent_data.get("responses", [])
    
    if isinstance(patterns, list) and isinstance(responses, list):
        conversation = []
        for pattern in patterns:
            conversation.append(pattern)
            conversation.extend(responses)  # Append all responses for each pattern
        trainer.train(conversation)
    else:
        print(f"Skipping invalid intent: {patterns}")