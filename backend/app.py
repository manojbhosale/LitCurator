""" code for singe QA system 
from flask import Flask, request, jsonify
from process_pdf import extract_text_from_pdf
from vector_store import store_documents, query_documents
from chatbot import generate_response
from summarizer import summarize_text

app = Flask(__name__)

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    file = request.files["pdf"]
    file_name = file.filename
    text_chunks = extract_text_from_pdf(file, file_name)
    store_documents(text_chunks)
    return jsonify({"message": "PDF processed and indexed successfully!"})

@app.route("/ask", methods=["POST"])
def ask():
    query = request.json["query"]
    references = query_documents(query)
    response = generate_response(query, [r["text"] for r in references])

    # Format references with page numbers
    formatted_references = [
        f"{r['file_name']} (Page {r['page']}): {r['text'][:200]}..."
        for r in references
    ]
    
    return jsonify({"answer": response, "references": formatted_references})

# Endpoint to summarize a research paper
@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json["text"]
    summary = summarize_text(text)
    return jsonify({"summary": summary})

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"summary": "hello  World!"})

if __name__ == "__main__":
    app.run(debug=True)
"""
    


# Code for converesational chatbot

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from process_pdf import extract_text_from_pdf
from vector_store import store_documents, query_documents
from chatbot import generate_response
from summarizer import summarize_text

app = Flask(__name__)
CORS(app)  # Allow frontend access
app.secret_key = "supersecretkey"  # Required for session storage

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    file = request.files["pdf"]
    file_name = file.filename
    text_chunks = extract_text_from_pdf(file, file_name)
    store_documents(text_chunks)
    return jsonify({"message": "PDF processed and indexed successfully!"})

@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json["query"]

    # Retrieve session chat history
    if "chat_history" not in session:
        session["chat_history"] = []

    references = query_documents(user_query)

    # Format chat history for context
    chat_history = session["chat_history"]
    history_text = "\n".join([f"User: {m['user']}\nBot: {m['bot']}" for m in chat_history])

    # Generate response with conversation context
    response = generate_response(user_query, [r["text"] for r in references], history_text)

    # Store new interaction in chat history
    session["chat_history"].append({"user": user_query, "bot": response})
    
    # Keep history limited (last 10 messages)
    session["chat_history"] = session["chat_history"][-10:]

    # Format references
    formatted_references = [
        f"{r['file_name']} (Page {r['page']}): {r['text'][:200]}..."
        for r in references
    ]

    return jsonify({"answer": response, "references": formatted_references, "history": session["chat_history"]})

if __name__ == "__main__":
    app.run(debug=True)
