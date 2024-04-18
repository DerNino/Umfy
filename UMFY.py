# Speichere diesen Code in einer Datei mit der Erweiterung ".py", z.B. "app.py"

import streamlit as st
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import random

# Modell und Tokenizer initialisieren
tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
model = GPT2LMHeadModel.from_pretrained("gpt2-medium")

def generate_survey_question():
    # Liste von Umfrage-Themen und zugehörigen Fragen
    survey_topics = {
        "Flugreisen": "Wie oft sind Sie im letzten Jahr geflogen?",
        "Essensausgaben": "Wie viel zahlen Sie täglich für Essen aus?"
        # Füge weitere Umfrage-Themen und Fragen hinzu, falls gewünscht
    }
    
    # Zufälliges Thema auswählen
    topic = random.choice(list(survey_topics.keys()))
    question = survey_topics[topic]
    
    # Generiere Antwortmöglichkeiten basierend auf dem gewählten Thema
    if topic == "Flugreisen":
        answer_options = ["1x", "2x", "3x", "4x oder mehr"]
    elif topic == "Essensausgaben":
        answer_options = ["Weniger als 10€", "10€-20€", "20€-30€", "Mehr als 30€"]
    # Füge weitere Antwortmöglichkeiten für andere Themen hinzu, falls gewünscht
    
    return topic, question, answer_options

# Führe die Streamlit-Anwendung aus
if __name__ == "__main__":
    topic, question, answer_options = generate_survey_question()
    
    st.write(f"Umfragefrage zum Thema '{topic}': {question}")
    
    # Zeige die Antwortmöglichkeiten als anklickbare Kästchen an
    selected_option = st.radio("Antwortmöglichkeiten:", answer_options)
    
    # Speichern-Button, um die ausgewählte Antwort zu speichern
    if st.button("Speichern"):
        st.write(f"Sie haben '{selected_option}' als Antwort gespeichert.")
