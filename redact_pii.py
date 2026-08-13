from docx import Document
from presidio_analyzer import AnalyzerEngine

def redact_docx(input_path, output_path):
    analyzer = AnalyzerEngine()
    doc = Document(input_path)
    for para in doc.paragraphs:
        results = analyzer.analyze(text=para.text, language='en')
        print(results)
