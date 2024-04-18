import streamlit as st
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import random
import time

# Bibliothek für das Diagramm importieren
import matplotlib.pyplot as plt

# Daten für das Diagramm
umfrage_ergebnisse = [25, 30, 20, 15, 10]
tage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']

# Diagramm erstellen
plt.bar(tage, umfrage_ergebnisse)

# Titel und Achsenbeschriftungen hinzufügen
plt.title('UMFY', color='purple')
plt.xlabel('Tage')
plt.ylabel('Umfrageergebnisse')
plt.text(0.5, -0.1, 'Eine Umfrage pro Tag', transform=plt.gca().transAxes, ha='center')

# Streamlit-Anwendung
st.pyplot()

# Modell und Tokenizer initialisieren
tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
model = GPT2LMHeadModel.from_pretrained("gpt2-medium")

def generate_survey_question():
    # Liste von Umfrage-Themen und zugehörigen Fragen
    survey_topics = {
        "Flugreisen": "Wie oft sind Sie im letzten Jahr geflogen?",
        "Essensausgaben": "Wie viel geben Sie durchschnittlich für Essen pro Mahlzeit aus?",
        "Autoverkehr": "Wie viele Kilometer fahren Sie täglich mit dem Auto?",
        "Sportaktivitäten": "Wie oft betreiben Sie körperliche Aktivitäten pro Woche?",
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
    elif topic in ["Essensausgaben"]:
        answer_options = ["Weniger als 5€", "5€-10€", "10€-20€", "Mehr als 20€"]
    elif topic in ["Einkaufsgewohnheiten"]:
        answer_options = ["Supermarkt", "Bauernmarkt", "Online", "Bioladen"]
    elif topic in ["Urlaubsziele"]:
        answer_options = ["Strandurlaub", "Städtereise", "Aktivurlaub", "Abenteuerreise"]
    elif topic in ["Freizeitaktivitäten"]:
        answer_options = ["Sport treiben", "Lesen", "Musik hören", "Gesellschaftsspiele spielen"]
    elif topic in ["Rauchgewohnheiten"]:
        answer_options = ["Ja", "Nein"]
    elif topic in ["Alkoholkonsum"]:
        answer_options = ["Gar nicht", "Gelegentlich", "Einmal pro Woche", "Mehrmals pro Woche"]
    # Füge weitere Antwortmöglichkeiten für andere Themen hinzu, falls gewünscht

    return topic, question, answer_options

# Führe die Streamlit-Anwendung aus
if __name__ == "__main__":
    topic, question, answer_options = generate_survey_question()

    st.write(f"Umfragefrage zum Thema '{topic}': {question}")

    # Zeige die Antwortmöglichkeiten als anklickbare Kästchen an
    selected_option = st.radio("Antwortmöglichkeiten:", answer_options)

    # Speicher-Button
    if st.button("Speichern"):
        st.write(f"Sie haben '{selected_option}' als Antwort gespeichert.")
        st.write("Vielen Dank fürs Mitmachen!")
