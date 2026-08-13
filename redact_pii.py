from docx import Document

def redact_docx(input_path, output_path):
    doc = Document(input_path)
    for para in doc.paragraphs:
        print(para.text)
