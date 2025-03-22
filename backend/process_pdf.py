import pdfplumber

# def extract_text_from_pdf(file):
#     text = ""
#     with pdfplumber.open(file) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"
#     return text

def extract_text_from_pdf(file, file_name):
    text_chunks = []
    with pdfplumber.open(file) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                text_chunks.append({"text": text, "page": page_num, "file_name": file_name})
    return text_chunks