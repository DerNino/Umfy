import firebase_admin
from firebase_admin import credentials, firestore

# Pfad zu Ihrer Firebase-Servicekonto-Schlüsseldatei
cred = credentials.Certificate("C:\Users\jajod\OneDrive\Desktop\Informatik ZHAW\umfy-53792-firebase-adminsdk-jbrce-399f5d85ba")
firebase_admin.initialize_app(cred)

# Firestore-Client initialisieren
db = firestore.client()
