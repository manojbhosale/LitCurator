from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import requests

GEMINI_API_KEY = "<GEMINI_API_KEY>"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def generate_response(query, references, history_text):
    context = "\n".join(references)
    
    # Include previous chat history for better context
    input_text = f"""
    Previous Conversation:
    {history_text}

    Research Context:
    {context}

    User Query: {query}
    Answer:
    """

    payload = payload = {
  "contents": [{
    "parts":[{"text": input_text}]
    }]
   }
    response = requests.post(API_URL,  json=payload)
    print("response JSON ====>>>> ",response.status_code, "\n",response.text)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.json()}"

