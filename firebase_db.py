import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase apenas se ainda não foi inicializado
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

def clear_flashcard_history():
    # Recupera todos os documentos da coleção
    docs = db.collection("flashcard_history").stream()
    # Deleta cada documento
    for doc in docs:
        doc.reference.delete()