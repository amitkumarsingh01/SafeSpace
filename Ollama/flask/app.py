from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from config import Config
from helpers.llm_helper import chat, stream_parser

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    with sqlite3.connect('chatbot.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                type TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                message TEXT,
                response TEXT
            )
        """)
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password, type) VALUES ('admin', '1234', 'admin')
        """)
        conn.commit()

init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('chatbot.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
        if user:
            session['username'] = user[1]
            session['type'] = user[3]
            if user[3] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('chatbot'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'username' not in session or session['type'] != 'admin':
        return redirect(url_for('login'))
    with sqlite3.connect('chatbot.db') as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            if 'delete' in request.form:
                user_id = request.form['delete']
                cursor.execute("DELETE FROM users WHERE id = ? AND username != 'admin'", (user_id,))
            if 'add' in request.form:
                username = request.form['username']
                password = request.form['password']
                user_type = request.form['type']
                cursor.execute("INSERT INTO users (username, password, type) VALUES (?, ?, ?)", (username, password, user_type))
            conn.commit()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return render_template('admin_dashboard.html', users=users)

@app.route('/chat', methods=['GET', 'POST'])
def chatbot():
    if 'username' not in session or session['type'] != 'user':
        return redirect(url_for('login'))
    username = session['username']
    with sqlite3.connect('chatbot.db') as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            user_message = request.form['user_message']
            with app.app_context():
                response_message = generate_response(user_message)  # Generate response using helpers
            cursor.execute("INSERT INTO chats (username, message, response) VALUES (?, ?, ?)", (username, user_message, response_message))
            conn.commit()
        cursor.execute("SELECT message, response FROM chats WHERE username = ?", (username,))
        chat_history = cursor.fetchall()
    return render_template('chatbot.html', chat_history=chat_history)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def generate_response(user_prompt):
    model = Config.OLLAMA_MODELS[0]  
    llm_stream = chat(user_prompt, model=model)
    response = "".join(stream_parser(llm_stream))  
    return response


class Config:
    PAGE_TITLE = "SafeSpace Chatbot"

    OLLAMA_MODELS = ('llama3.2:latest',)  

    SYSTEM_PROMPT = f"""
        You are a helpful medical mental health chatbot that has access to the following 
        open-source models: {', '.join(OLLAMA_MODELS)}.
        
        You can answer questions for users on any health, mental health, and medical topics.
        For any other questions unrelated to medical or mental health, respond with:
        "Please ask medical or mental health-related questions."
    """


if __name__ == '__main__':
    app.run(debug=True)
