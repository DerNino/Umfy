import firebase_admin
from firebase_admin import credentials, firestore

# Pfad zu Ihrer Firebase-Servicekonto-Schlüsseldatei
cred = credentials.Certificate("path/to/your/firebase/credentials.json")
firebase_admin.initialize_app(cred)

# Firestore-Client initialisieren
db = firestore.client()
