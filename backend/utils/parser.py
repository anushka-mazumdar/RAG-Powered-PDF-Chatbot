from PyPDF2 import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages])

