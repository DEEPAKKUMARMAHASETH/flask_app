from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get credentials from .env
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "test_db")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["form_data"]

# API route to read from backend file
@app.route('/api')
def get_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

# Homepage with form
@app.route('/')
def index():
    return render_template('index.html', error=None)

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')
        email = request.form.get('email')

        if not name or not email:
            return render_template('index.html', error="All fields are required")

        collection.insert_one({"name": name, "email": email})
        return redirect(url_for('success'))

    except Exception as e:
        return render_template('index.html', error=str(e))

# Success page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
