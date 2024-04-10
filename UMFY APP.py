import streamlit as st

# Counter für die Anzahl der Teilnehmer
participants = 0

# Funktion zum Zählen der Teilnehmer
def count_participants():
    global participants
    participants += 1

# App-Layout
st.title("Umfrage-App")

# Tägliche Umfrage
st.header("Tägliche Umfrage")
question = st.text_input("Frage:")
option1 = st.text_input("Option 1:")
option2 = st.text_input("Option 2:")
option3 = st.text_input("Option 3:")
vote_button = st.button("Abstimmen")

# Anzeige der Teilnehmeranzahl
st.sidebar.header("Teilnehmer heute")
st.sidebar.write(f"Teilnehmer: {participants}")

# Ergebnisse der letzten Umfrage
st.sidebar.header("Ergebnisse der letzten Umfrage")
st.sidebar.write("Option 1: xx%")
st.sidebar.write("Option 2: xx%")
st.sidebar.write("Option 3: xx%")

# Einwilligung
consent = st.checkbox("Ich stimme der Verwendung meiner Daten zu")
accept_button = st.button("Akzeptieren")

# Teilnehmerzählung aktualisieren, wenn abgestimmt wird
if vote_button:
    count_participants()

# Logik für Akzeptieren-Button
if accept_button:
    if consent:
        st.write("Vielen Dank für Ihre Einwilligung!")
    else:
        st.write("Bitte stimmen Sie der Verwendung Ihrer Daten zu.")

