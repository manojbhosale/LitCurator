import streamlit as st
import requests

st.title("Conversational Medical Research Chatbot")

# Upload PDF
st.header("Upload Research Paper")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file:
    files = {"pdf": uploaded_file}
    response = requests.post("http://127.0.0.1:5000/upload_pdf", files=files)
    st.success(response.json()["message"])

# Chat Section
st.header("Chat with Research Papers")

# Store chat history in session state
if "history" not in st.session_state:
    st.session_state["history"] = []

# Ready-to-use prompts
st.subheader("Quick Questions:")
col1, col2 = st.columns(2)

if col1.button("Summarize the key findings"):
    query = "Summarize the key findings of the research papers."
elif col2.button("List potential medical applications"):
    query = "List potential medical applications based on the research papers."
else:
    query = st.text_input("Enter your question:")

if st.button("Get Answer") or query:
    response = requests.post("http://127.0.0.1:5000/ask", json={"query": query})
    data = response.json()

    # Update history
    st.session_state["history"].append({"user": query, "bot": data["answer"]})

    # Display chat history
    st.subheader("Conversation History")
    for chat in st.session_state["history"]:
        st.markdown(f"**User:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")
        st.write("---")

    # Show References
    st.subheader("References")
    for ref in data["references"]:
        st.write("- ", ref)
