import requests
from dotenv import load_dotenv
from models.note import Note
from urllib.parse import urlparse
import os

load_dotenv()


def get_text_notes(topic_id: int, db):
    notes = db.query(Note).filter_by(topic_id=topic_id, content_type='text').all()
    return [note.content for note in notes]

def get_image_notes(topic_id: int, db):
    notes = db.query(Note).filter_by(topic_id=topic_id, content_type='image').all()
    return [note.image_url for note in notes]

def ocr_space_image_file(image_url: str, key: str = 'helloworld'):
    if image_url.startswith('/'):
        local_path = f"./{image_url.lstrip('/')}"
        if not os.path.exists(local_path):
            return f"Błąd: plik {local_path} nie istnieje."
        with open(local_path, "rb") as img_file:
            files = {'file': ('image.png', img_file)}
            payload = {'language': 'pol', 'isOverlayRequired': False}
            headers = {'apikey': key}
            response = requests.post('https://api.ocr.space/parse/image', files=files, data=payload, headers=headers)
            result = response.json()
            if result.get('ParsedResults'):
                return result['ParsedResults'][0]['ParsedText']
            else:
                return f"Błąd OCR: {result.get('ErrorMessage', 'Unknown Error')}"
    else:
        img_response = requests.get(image_url, timeout=10)
        if img_response.status_code != 200:
            return f"Błąd pobierania obrazu: {img_response.status_code}"
        files = {'file': ('image.png', img_response.content)}
        payload = {'language': 'pol', 'isOverlayRequired': False}
        headers = {'apikey': key}
        response = requests.post('https://api.ocr.space/parse/image', files=files, data=payload, headers=headers)
        result = response.json()
        if result.get('ParsedResults'):
            return result['ParsedResults'][0]['ParsedText']
        else:
            return f"Błąd OCR: {result.get('ErrorMessage', 'Unknown Error')}"

def get_all_image_notes(topic_id: int, db):
    image_urls = get_image_notes(topic_id, db)
    list_of_text_notes = []
    for url in image_urls:
        try:
            text = ocr_space_image_file(url)
            if isinstance(text, str):
                text = text.replace('\r', '').replace('\n', ' ')
            list_of_text_notes.append(text)
        except Exception as e:
            list_of_text_notes.append(f"Błąd OCR: {e}")
    return list_of_text_notes

def get_all_notes(topic_id: int, db):
    text_notes = get_text_notes(topic_id, db)
    image_notes = get_all_image_notes(topic_id, db)
    return text_notes + image_notes

def summarize_notes_with_deepseek(topic_id: int, db):
    notes = get_all_notes(topic_id, db)
    if not notes:
        return "Brak notatek do podsumowania."
    prompt = (
        "Oto lista notatek z danego tematu. Na ich podstawie wygeneruj krótkie podsumowanie najważniejszych informacji:\n\n"
        + "\n".join(f"- {note}" for note in notes)
        + "Pisz w języku polskim i nie używaj emotikonów. Najlepiej staraj się zamykać w paru zdaniach\n\n"
        + "Nie pisz nic poza podsumowaniem, nie pisz też, że to jest podsumowanie. "
    )
    api_key = os.getenv("DEEPSEEK_API_KEY")
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Jesteś pomocnym asystentem edukacyjnym."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return f"Błąd DeepSeek API: {response.status_code} - {response.text}"
    result = response.json()
    return result["choices"][0]["message"]["content"]
