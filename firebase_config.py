import firebase_admin
from firebase_admin import credentials, firestore

# Pfad zu Ihrer Firebase-Servicekonto-Schlüsseldatei
cred = credentials.Certificate("C:\Users\jajod\OneDrive\Desktop\Informatik ZHAW\umfy-53792-firebase-adminsdk-jbrce-7bbf56e5de.json")
firebase_admin.initialize_app(cred)

# Firestore-Client initialisieren
db = firestore.client()
