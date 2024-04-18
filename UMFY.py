# Speichere diesen Code in einer Datei mit der Erweiterung ".py", z.B. "app.py"

import streamlit as st
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import random

# Modell und Tokenizer initialisieren
tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
model = GPT2LMHeadModel.from_pretrained("gpt2-medium")

def generate_social_question():
    # Liste von sozialkritischen Themen
    topics = [
        "Umweltschutz",
        "Menschenrechte",
        "Soziale Gerechtigkeit",
        "Klimawandel",
        "Gesellschaftliche Ungleichheit",
        "Globalisierung"
    ]
    
    # Zufälliges Thema auswählen
    topic = random.choice(topics)
    
    # Prompt für die Frageerstellung
    prompt = f"Stelle eine Frage zum Thema '{topic}':"
    
    # Kodiere das Eingabe-Prompt
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    # Generiere eine Frage mit dem Modell
    output = model.generate(
        input_ids,
        max_length=150,  # Erhöhe die maximale Länge der generierten Sequenz
        num_return_sequences=1,
        temperature=0.8,  # Ändere die Temperatur für variablere Ausgaben
        top_p=0.95,  # Verwende Top-p Sampling für variablere Ausgaben
        repetition_penalty=1.2  # Erhöhe die Repetition Penalty, um Wiederholungen zu verringern
    )
    
    # Dekodiere die generierte Frage
    question = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    # Generiere vier Antwortmöglichkeiten mit dem Modell
    answer_options = []
    for _ in range(4):
        output = model.generate(
            input_ids,
            max_length=50,  # Erhöhe die maximale Länge der generierten Sequenz für die Antwortmöglichkeiten
            num_return_sequences=1,
            temperature=0.8,  # Ändere die Temperatur für variablere Ausgaben
            top_p=0.95,  # Verwende Top-p Sampling für variablere Ausgaben
            repetition_penalty=1.2  # Erhöhe die Repetition Penalty, um Wiederholungen zu verringern
        )
        answer = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        answer_options.append(answer)
    
    return question, topic, answer_options

# Führe die Streamlit-Anwendung aus
if __name__ == "__main__":
    question, topic, answer_options = generate_social_question()
    
    # Anzahl der bereits abgestimmten Personen
    num_votes = st.session_state.get("num_votes", 0)
    
    st.write(f"Frage zum Thema '{topic}': {question}")
    st.write("Antwortmöglichkeiten:")
    for i, answer in enumerate(answer_options):
        st.write(f"{i+1}. {answer}")
    
    # Popup-Feld mit der Anzahl der bereits abgestimmten Personen
    if st.button("Anzeigen"):
        st.sidebar.text(f"Bereits abgestimmt: {num_votes} Personen")
