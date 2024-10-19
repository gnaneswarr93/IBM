import requests
import sqlite3
import os


# Placeholder API key (replace with a valid one when available)
API_KEY = "AIzaSyDfG5MxG15fV7KQuErL4ALG3ucbROQlVV0"
# API URL updated (replace with the appropriate model and endpoint as per API documentation)
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'

def create_chat_message(message, is_user):
    role = "user" if is_user else "assistant"
    return {"contents": [{"role": role, "parts": [{"text": message}]}]}

def generate_response(user_message):
    request_data = create_chat_message(user_message, True)
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, headers=headers, json=request_data)
        response.raise_for_status()  # Raise exception for non-200 status codes
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        print(f"Error generating response: {e}")
        return "An error occurred. Please try again later."

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

def main():
    while True:
        user_message = input("You: ")
        if user_message.lower() == "quit":
            break
        assistant_message = generate_response(user_message)
        print(f"Assistant: {assistant_message}")

if __name__ == "__main__":
    print("Welcome to your AI Assistant!")
    main()
