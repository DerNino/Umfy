import streamlit as st
import requests
import json
import base64
import datetime

# Funktion, um Fragen von GitHub zu laden
def load_questions():
    url = f"https://api.github.com/repos/{st.secrets['GITHUB_REPO']}/contents/{st.secrets['FRAGEN_PATH']}"
    token = st.secrets['GITHUB_TOKEN']
    headers = {'Authorization': f'token {token}'}  # Korrektur hier
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = base64.b64decode(response.json()['content']).decode('utf-8')
        return eval(content)
    else:
        st.error("Fehler beim Laden der Fragen.")
        return []

# Antworten auf GitHub speichern oder aktualisieren
def save_answer_to_github(content):
    url = f"https://api.github.com/repos/{st.secrets['GITHUB_REPO']}/contents/{st.secrets['ANTWORTEN_PATH']}"
    token = st.secrets['GITHUB_TOKEN']
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        sha = r.json()['sha']
        old_content = base64.b64decode(r.json()['content']).decode('utf-8')
        new_content = old_content + f",\n'{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}': '{content}'"
    else:
        new_content = f"answers = [\n'{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}': '{content}'\n]"
        sha = None
    
    data = {
        'message': f"Antwort aktualisiert am {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        'content': base64.b64encode(new_content.encode()).decode('utf-8'),
        'sha': sha
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        st.success("Antwort erfolgreich auf GitHub gespeichert!")
    else:
        st.error("Fehler beim Speichern der Antwort: " + response.json().get('message', ''))

# Streamlit App Interface
st.title("Tägliche Frage")
fragen = load_questions()
if fragen:
    today = datetime.date.today().toordinal()
    frage = fragen[today % len(fragen)]
    st.write(f"Frage des Tages: {frage}")

    answer = st.text_area("Deine Antwort:")
    if st.button("Antwort speichern"):
        save_answer_to_github(answer)
