import streamlit as st
import random
import datetime
import pandas as pd
import os
import json
from googletrans import Translator
from werkzeug.security import generate_password_hash, check_password_hash

# CSV-Datei für die Fragen
CSV_FILE = "questions.csv"

# JSON-Dateien für Benutzer und Antworten
USERS_FILE = "users.json"
RESPONSES_FILE = "responses.json"

# Dummy-Benutzer für die Anmeldung (in einer echten Anwendung würden Sie eine Datenbank verwenden)
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as file:
        users = json.load(file)
else:
    users = {}

# Antworten-Speicherung (in einer echten Anwendung würden Sie eine Datenbank verwenden)
if os.path.exists(RESPONSES_FILE):
    with open(RESPONSES_FILE, 'r') as file:
        responses = {datetime.datetime.strptime(k, "%Y-%m-%d").date(): v for k, v in json.load(file).items()}
else:
    responses = {}

# Benutzer speichern
def save_users():
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

# Antworten speichern
def save_responses():
    with open(RESPONSES_FILE, 'w') as file:
        json.dump({k.strftime("%Y-%m-%d"): v for k, v in responses.items()}, file)

# Laden der Fragen aus einer CSV-Datei
def load_questions_from_csv(file_path):
    if not os.path.exists(file_path):
        st.error(f"Die Datei {file_path} wurde nicht gefunden.")
        return []
    try:
        questions_df = pd.read_csv(file_path, encoding='utf-8')
        if 'question' not in questions_df.columns:
            st.error(f"Die Datei {file_path} enthält nicht die erwartete Spalte 'question'.")
            return []
        return questions_df['question'].dropna().tolist()
    except pd.errors.ParserError as e:
        st.error(f"Fehler beim Parsen der Datei {file_path}: {e}")
        return []
    except Exception as e:
        st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return []

# Übersetzung von Text
def translate_text(text, target_language="de"):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

# UI für die Anmeldung
def login_ui():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username in users and check_password_hash(users[username], password):
            st.session_state['username'] = username
            st.session_state['register'] = False
            st.sidebar.success("Login erfolgreich!")
        else:
            st.sidebar.error("Ungültiger Benutzername oder Passwort")
    
    if st.sidebar.button("Register"):
        st.session_state['register'] = True

# UI für die Registrierung
def register_ui():
    st.sidebar.title("Registrieren")
    username = st.sidebar.text_input("Wählen Sie einen Benutzernamen")
    password = st.sidebar.text_input("Wählen Sie ein Passwort", type="password")
    confirm_password = st.sidebar.text_input("Passwort bestätigen", type="password")
    if st.sidebar.button("Registrieren"):
        if password != confirm_password:
            st.sidebar.error("Passwörter stimmen nicht überein")
        elif username in users:
            st.sidebar.error("Benutzername existiert bereits")
        else:
            users[username] = generate_password_hash(password)
            save_users()
            st.session_state['username'] = username
            st.session_state['register'] = False
            st.sidebar.success("Registrierung erfolgreich! Sie sind jetzt eingeloggt.")
            st.experimental_rerun()  # Erzwinge das Neuladen der Seite, um die Umfrage-UI anzuzeigen

# Generierung eines zufälligen Namens
def generate_fake_name():
    first_names = ["John", "Emily", "Michael", "Sophia", "William", "Emma", "James", "Olivia", "Benjamin", "Isabella"]
    last_names = ["Smith", "Johnson", "Brown", "Miller", "Davis", "Garcia", "Wilson", "Taylor", "Anderson", "Thomas"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Tägliche Frage erhalten
def get_daily_question():
    questions = load_questions_from_csv(CSV_FILE)
    if not questions:
        return "Keine Frage verfügbar"
    return random.choice(questions)

# Streamlit UI
def streamlit_ui():
    if 'register' not in st.session_state:
        st.session_state['register'] = False

    if st.session_state['register']:
        register_ui()
    elif 'username' not in st.session_state:
        login_ui()
    else:
        st.title("UMFY App")
        st.write("Willkommen bei der UMFY App.")

        today = datetime.date.today()
        daily_question = get_daily_question()
        st.write("Frage des Tages:", daily_question)

        # Eingabe und Speicherung der Nutzerantworten
        user_response = st.text_input("Ihre Antwort:")
        if st.button("Antwort senden"):
            if today not in responses:
                responses[today] = {'question': daily_question, 'answers': []}
            responses[today]['answers'].append({'name': generate_fake_name(), 'response': user_response, 'replies': []})
            save_responses()
            st.success("Ihre Antwort wurde gespeichert.")

        # Anzeigen aller Antworten des heutigen Tages
        if today in responses:
            st.write("Antworten für heute:")
            for idx, answer in enumerate(responses[today]['answers']):
                st.text(f"{answer['name']}: {answer['response']}")
                if st.button(f"Antworten an {answer['name']}", key=f"reply_button_{idx}"):
                    reply = st.text_input(f"Ihre Antwort an {answer['name']}", key=f"reply_input_{idx}")
                    if st.button("Antwort senden", key=f"send_reply_button_{idx}"):
                        answer['replies'].append(reply)
                        save_responses()

        # UI für das Durchsuchen vergangener Antworten
        with st.sidebar:
            past_date = st.date_input("Durchsuchen vergangener Daten", value=today, min_value=min(responses.keys(), default=today), max_value=today)
            if past_date in responses:
                st.write(f"Frage vom {past_date}: {responses[past_date]['question']}")
                for answer in responses[past_date]['answers']:
                    st.text(answer['response'])
                    for reply in answer['replies']:
                        st.text(f" - {reply}")

if __name__ == "__main__":
    streamlit_ui()
