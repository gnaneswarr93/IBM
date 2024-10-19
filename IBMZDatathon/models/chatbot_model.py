import sqlite3
import os
import requests

# Initialize Gemini API client
GEMINI_API_URL = "https://api.gemini.com/v1/chat/completions"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_mental_health_reply(user_message):
    try:
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            "model": "gemini-1.0",  # Replace with the appropriate model name
        }
        
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        chat_response = response.json()
        return chat_response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error in Gemini API: {e}")
        return "I'm sorry, I couldn't process your request."

def create_connection():
    connection = sqlite3.connect("chatbot.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS conversations 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_message TEXT, bot_reply TEXT)''')
    connection.commit()
    return connection

def log_conversation(user_message, bot_reply):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (user_message, bot_reply) VALUES (?, ?)", (user_message, bot_reply))
    conn.commit()
    conn.close()

def get_past_conversations():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_reply FROM conversations")
    rows = cursor.fetchall()
    conn.close()
    return rows