# Speichere diesen Code in einer Datei mit der Erweiterung ".py", z.B. "app.py"

import streamlit as st
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import random
import time

# Modell und Tokenizer initialisieren
tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
model = GPT2LMHeadModel.from_pretrained("gpt2-medium")

def generate_survey_question():
    # Liste von Umfrage-Themen und zugehörigen Fragen
    survey_topics = {
        "Flugreisen": "Wie oft sind Sie im letzten Jahr geflogen?",
        "Essensausgaben": "Wie viel zahlen Sie täglich für Essen aus?",
        "Autoverkehr": "Wie viele Kilometer fahren Sie täglich mit dem Auto?",
        "Sportaktivitäten": "Wie oft treiben Sie Sport pro Woche?",
        "Bildschirmzeit": "Wie viele Stunden verbringen Sie täglich vor Bildschirmen?",
        "Einkaufsgewohnheiten": "Wo kaufen Sie am häufigsten Lebensmittel ein?",
        "Urlaubsziele": "Welche Art von Urlaub bevorzugen Sie am meisten?",
        "Freizeitaktivitäten": "Was unternehmen Sie am liebsten in Ihrer Freizeit?",
        "Gesundheitsvorsorge": "Wie oft gehen Sie zur Vorsorgeuntersuchung?",
        "Nutzung von Öffentlichen Verkehrsmitteln": "Wie oft nutzen Sie öffentliche Verkehrsmittel?",
        "Arbeitszeit": "Wie viele Stunden arbeiten Sie durchschnittlich pro Woche?",
        "Fernsehgewohnheiten": "Wie viele Stunden fernsehen Sie täglich?",
        "Social Media Nutzung": "Wie viel Zeit verbringen Sie täglich auf Social Media Plattformen?",
        "Rauchgewohnheiten": "Rauchen Sie?",
        "Alkoholkonsum": "Wie oft trinken Sie Alkohol in der Woche?"
    }
    
    # Zufälliges Thema auswählen
    topic = random.choice(list(survey_topics.keys()))
    question = survey_topics[topic]
    
    # Generiere Antwortmöglichkeiten basierend auf dem gewählten Thema
    if topic in ["Flugreisen", "Autoverkehr", "Sportaktivitäten", "Bildschirmzeit", "Gesundheitsvorsorge", 
                 "Nutzung von Öffentlichen Verkehrsmitteln", "Arbeitszeit", "Fernsehgewohnheiten", "Social Media Nutzung"]:
        answer_options = ["Weniger als 1x pro Woche", "1-2x pro Woche", "3-4x pro Woche", "Mehr als 4x pro Woche"]
    elif topic in ["Essensausgaben", "Einkaufsgewohnheiten", "Freizeitaktivitäten", "Urlaubsziele"]:
        answer_options = ["Weniger als 10€", "10€-20€", "20€-30€", "Mehr als 30€"]
    elif topic in ["Rauchgewohnheiten"]:
        answer_options = ["Ja", "Nein"]
    elif topic in ["Alkoholkonsum"]:
        answer_options = ["Gar nicht", "1-2 mal", "3-4 mal", "Mehr als 4 mal"]
    # Füge weitere Antwortmöglichkeiten für andere Themen hinzu, falls gewünscht
    
    return topic, question, answer_options

# Führe die Streamlit-Anwendung aus
if __name__ == "__main__":
    topic, question, answer_options = generate_survey_question()
    
    st.write(f"Umfragefrage zum Thema '{topic}': {question}")
    
    # Zeige die Antwortmöglichkeiten als anklickbare Kästchen an
    selected_option = st.radio("Antwortmöglichkeiten:", answer_options)
    
    # Speichern-Button, um die ausgewählte Antwort zu speichern und zur "Danke"-Seite zu wechseln
    if st.button("Speichern"):
        st.write(f"Sie haben '{selected_option}' als Antwort gespeichert.")
        st.write("Vielen Dank fürs Mitmachen!")
        
        # Weiterleitung nach 2 Sekunden
        time.sleep(2)
        st.experimental_rerun()
