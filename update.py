from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load existing intents.json
def load_intents():
    try:
        with open('intents.json', 'r') as file:
            intents = json.load(file)
    except FileNotFoundError:
        intents = {"intents": []}
    return intents

# Save intents to intents.json
def save_intents(intents):
    with open('intents.json', 'w') as file:
        json.dump(intents, file, indent=4)

@app.route('/')
def frame_content():
    # Reading the update.html page
    with open('update.html', 'r') as f:
        content = f.read()
    return content

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

if __name__ == '__main__':
    app.run(debug=True)