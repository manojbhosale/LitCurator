from transformers import pipeline

summarizer = pipeline("summarization", model="t5-small")

# def summarize_text(text):
#     return summarizer(text, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]


import requests

HUGGING_FACE_API_TOKEN = "<Huggingface_API_Token>"
API_URL = "https://api-inference.huggingface.co/models/t5-small"

headers = {"Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"}

def summarize_text(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.json()}"
