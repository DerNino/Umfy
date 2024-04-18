import streamlit as st
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import random

# Modell und Tokenizer initialisieren (Fehlerbehandlung wird hier nicht benötigt)
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
    
    return question, topic
