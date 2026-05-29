from flask import Flask, render_template, request, jsonify,redirect
from datetime import datetime
import webbrowser
import sqlite3
import pyttsx3
import speech_recognition as sr
app = Flask(__name__)
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
def take_voice():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text

    except:
        return "Sorry, voice not recognized"    
# DATABASE
conn = sqlite3.connect('alexa.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    bot_reply TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    gmail TEXT,

    password TEXT
)
''')

conn.commit()


# ALEXA FUNCTION
def alexa_reply(message):

    message = message.lower()

    if 'hello' in message:
        return 'Hello! I am your mini Alexa.'

    elif 'time' in message:
        current_time = datetime.now().strftime('%I:%M %p')
        return f'The time is {current_time}'

    elif 'date' in message:
        current_date = datetime.now().strftime('%d %B %Y')
        return f'Today is {current_date}'

    elif 'google' in message:
        webbrowser.open('https://www.google.com')
        return 'Opening Google'

    elif 'youtube' in message:
        webbrowser.open('https://www.youtube.com')
        return 'Opening YouTube'

    elif 'instagram' in message:
        webbrowser.open('https://www.instagram.com')
        return 'Opening Instagram'

    elif 'weather' in message:
        return 'Today weather is pleasant.'

    elif 'bye' in message:
        return 'Goodbye!'
    
    elif 'spotify' in message:
        webbrowser.open('https://spotify.com')
        return 'Opening Spotify'

    elif 'chatgpt' in message:
        webbrowser.open('https://chat.openai.com')
        return 'Opening ChatGPT'

    else:
        return 'Sorry, I did not understand.'


# LOGIN PAGE
@app.route('/')
def login_page():

    return render_template('login.html')


# LOGIN FUNCTION
@app.route('/login', methods=['POST'])
def login():

    gmail = request.form['gmail']

    password = request.form['password']

    # SAVE USER IN DATABASE
    cursor.execute(

        'INSERT INTO users (gmail, password) VALUES (?, ?)',

        (gmail, password)
    )

    conn.commit()

    return redirect('/alexa')


# ALEXA PAGE
@app.route('/alexa')
def alexa():

    return render_template('index.html')


# CHAT API
@app.route('/chat', methods=['POST'])
def chat():

    data = request.json

    user_message = data['message']

    bot_reply = alexa_reply(user_message)
    speak(bot_reply)
    # SAVE TO DATABASE
    cursor.execute(
        'INSERT INTO chats (user_message, bot_reply) VALUES (?, ?)',
        (user_message, bot_reply)
    )

    conn.commit()

    return jsonify({'reply': bot_reply})

# RUN APP
if __name__ == '__main__':
    app.run(debug=True)