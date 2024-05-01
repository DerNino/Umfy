import streamlit as st
import random
import datetime
import requests

# DeepL API-Zugriffsdaten
DEEPL_API_KEY = "YOUR_DEEPL_API_KEY"

# Dies ist für die Speicherung von Antworten und deren Antworten.
responses = {}

def generate_fake_name():
    first_names = ["John", "Emily", "Michael", "Sophia", "William", "Emma", "James", "Olivia", "Benjamin", "Isabella"]
    last_names = ["Smith", "Johnson", "Brown", "Miller", "Davis", "Garcia", "Wilson", "Taylor", "Anderson", "Thomas"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def get_daily_question(language):
    today = datetime.date.today()
    # Verwende den heutigen Tag als Seed, um sicherzustellen, dass die gleiche Frage für alle Benutzer generiert wird
    random.seed(today.toordinal())
    return translate_text("What is your favorite book and why?", language)

def translate_text(text, target_language):
    url = "https://api.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_language
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        translation = response.json()["translations"][0]["text"]
        return translation
    else:
        return text  # Rückgabe des ursprünglichen Textes im Fehlerfall

def streamlit_ui():
    languages = ["en", "fr", "de", "it"]
    language = st.sidebar.selectbox("Language / Langue / Sprache / Lingua", languages)

    st.title("UMFY App")
    st.write(translate_text("Welcome to the UMFY App.", language))

    today = datetime.date.today()
    daily_question = get_daily_question(language)
    st.write(translate_text("Question of the day:", language), daily_question)

    # Eingabe und Speicherung der Nutzerantworten
    user_response = st.text_input(translate_text("Your answer:", language))
    if st.button(translate_text("Send answer", language)):
        if today not in responses:
            responses[today] = {'question': daily_question, 'answers': []}
        responses[today]['answers'].append({'name': generate_fake_name(), 'response': user_response, 'replies': []})
        st.success(translate_text("Your answer has been saved.", language))

    # Anzeigen aller Antworten des heutigen Tages
    if today in responses:
        st.write(translate_text("Answers for today:", language))
        for idx, answer in enumerate(responses[today]['answers']):
            st.text(f"{answer['name']}: {answer['response']}")
            if st.button(f"{translate_text('Reply to', language)} {answer['name']}"):
                reply = st.text_input(f"{translate_text('Your reply to', language)} {answer['name']}", key=f"reply{idx + 1}")
                if st.button(translate_text("Send", language), key=f"send{idx + 1}"):
                    answer['replies'].append(reply)

    # UI für das Durchsuchen vergangener Antworten
    with st.sidebar:
        past_date = st.date_input(translate_text("Browse past dates", language), value=today, min_value=min(responses.keys(), default=today), max_value=today)
        if past_date in responses:
            st.write(f"{translate_text('Question from', language)} {past_date}: {responses[past_date]['question']}")
            for answer in responses[past_date]['answers']:
                st.text(answer['response'])
                for reply in answer['replies']:
                    st.text(f" - {reply}")

if __name__ == "__main__":
    streamlit_ui()
