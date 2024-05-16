import streamlit as st
import random
import datetime
import pandas as pd
from googletrans import Translator
from werkzeug.security import generate_password_hash, check_password_hash

# CSV-Datei für die Fragen
CSV_FILE = "questions.csv"

# Dummy-Benutzer für die Anmeldung (in einer echten Anwendung würden Sie eine Datenbank verwenden)
users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2"),
}

# Antworten-Speicherung (in einer echten Anwendung würden Sie eine Datenbank verwenden)
responses = {}

# Laden der Fragen aus einer CSV-Datei
def load_questions_from_csv(file_path):
    questions_df = pd.read_csv(file_path)
    return questions_df['question'].tolist()

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
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("Invalid username or password")

# Generierung eines zufälligen Namens
def generate_fake_name():
    first_names = ["John", "Emily", "Michael", "Sophia", "William", "Emma", "James", "Olivia", "Benjamin", "Isabella"]
    last_names = ["Smith", "Johnson", "Brown", "Miller", "Davis", "Garcia", "Wilson", "Taylor", "Anderson", "Thomas"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Tägliche Frage erhalten
def get_daily_question():
    questions = load_questions_from_csv(CSV_FILE)
    return random.choice(questions)

# Streamlit UI
def streamlit_ui():
    if 'username' not in st.session_state:
        login_ui()
        return

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
