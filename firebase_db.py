import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_flashcards(text, flashcards):
    doc_ref = db.collection("flashcard_history").document()
    doc_ref.set({
        "input_text": text,
        "flashcards": flashcards,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return doc_ref.id

def get_flashcard_history():
    docs = db.collection("flashcard_history").order_by("timestamp", direction="DESCENDING").limit(10).get()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]