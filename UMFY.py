import streamlit as st
import random
import datetime
from googletrans import Translator

# Liste von 100 sozialkritischen Fragen
social_questions = [
    "Was denkst du über die soziale Ungleichheit in unserer Gesellschaft?",
   "Welche Maßnahmen könnten ergriffen werden, um Armut zu bekämpfen?",
   "Wie können wir die Bildungschancen für alle verbessern?",
   "Welche Rolle spielt die Regierung bei der Lösung sozialer Probleme?",
   "Wie können wir die Gleichstellung der Geschlechter vorantreiben?",
   "Was können wir tun, um die Diskriminierung von Minderheiten zu verringern?",
   "Wie beeinflusst soziale Ungerechtigkeit das Wirtschaftswachstum?",
   "Welche Veränderungen könnten die Lebensqualität für alle verbessern?",
   "Wie können wir sicherstellen, dass jeder Zugang zu angemessener Gesundheitsversorgung hat?",
   "Welche Auswirkungen hat Umweltverschmutzung auf benachteiligte Gemeinschaften?",
   "Wie können wir den Klimawandel bekämpfen und gleichzeitig soziale Gerechtigkeit fördern?",
   "Welche Rolle spielen Unternehmen bei der Lösung sozialer Probleme?",
   "Wie können wir die Obdachlosigkeit in unserer Gemeinschaft reduzieren?",
   "Wie können wir die soziale Isolation älterer Menschen bekämpfen?",
    "Welche Auswirkungen hat der Zugang zu sauberem Wasser auf die Gesundheit von Gemeinschaften?",
    "Wie können wir die Ausbeutung von Arbeitskräften in globalen Lieferketten verhindern?",
    "Was sind die Ursachen von sozialer Ausgrenzung und wie können wir sie bekämpfen?",
    "Welche Rolle spielt Bildung bei der Schaffung einer gerechteren Gesellschaft?",
    "Wie können wir die digitale Kluft zwischen verschiedenen Bevölkerungsgruppen überwinden?",
    "Welche Maßnahmen können ergriffen werden, um die soziale Mobilität zu erhöhen?",
]

# Dies ist für die Speicherung von Antworten und deren Antworten.
responses = {}

def generate_fake_name():
    first_names = ["John", "Emily", "Michael", "Sophia", "William", "Emma", "James", "Olivia", "Benjamin", "Isabella"]
    last_names = ["Smith", "Johnson", "Brown", "Miller", "Davis", "Garcia", "Wilson", "Taylor", "Anderson", "Thomas"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def get_daily_question(language):
    return translate_text(random.choice(social_questions), language)

def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

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
