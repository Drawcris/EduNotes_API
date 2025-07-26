import os
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()


def get_text_notes(topic_id: int):
    response = requests.get("http://127.0.0.1:8000/notes/")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch notes: {response.status_code} - {response.text}")
    r_json = response.json()
    list_of_notes = []
    for note in r_json:
        if note["topic_id"] == topic_id and note['content_type'] == 'text':
            list_of_notes.append(note['content'])
    return list_of_notes

def get_image_notes(topic_id: int):
    response = requests.get("http://127.0.0.1:8000/notes/")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch notes: {response.status_code} - {response.text}")
    r_json = response.json()
    list_of_notes = []
    for note in r_json:
        if note["topic_id"] == topic_id and note['content_type'] == 'image':
            list_of_notes.append(note['image_url'])
    return list_of_notes

def ocr_space_image_file(image_url: str, api_key: str = 'helloworld'):
    if image_url.startswith('/'):
        image_url = f"http://127.0.0.1:8000{image_url}"
    img_response = requests.get(image_url)
    if img_response.status_code != 200:
        return f"Błąd pobierania obrazu: {img_response.status_code}"
    files = {'file': ('image.png', img_response.content)}
    payload = {'language': 'pol', 'isOverlayRequired': False}
    headers = {'apikey': api_key}
    response = requests.post('https://api.ocr.space/parse/image', files=files, data=payload, headers=headers)
    result = response.json()
    if result.get('ParsedResults'):
        return result['ParsedResults'][0]['ParsedText']
    else:
        return f"Błąd OCR: {result.get('ErrorMessage', 'Unknown Error')}"

def get_all_image_notes(topic_id: int):
    image_urls = get_image_notes(topic_id)
    list_of_text_notes = []
    for url in image_urls:
        try:
            text = ocr_space_image_file(url)
            # Usuwanie \r i zamiana \n na spację
            if isinstance(text, str):
                text = text.replace('\r', '').replace('\n', ' ')
            list_of_text_notes.append(text)
        except Exception as e:
            list_of_text_notes.append(f"Błąd OCR: {e}")
    return list_of_text_notes

def get_all_notes(topic_id: int):
    text_notes = get_text_notes(topic_id)
    image_notes = get_all_image_notes(topic_id)
    return text_notes + image_notes
