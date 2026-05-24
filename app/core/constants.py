"""
Application constants
"""

# Response messages
SUCCESS_MESSAGES = {
    "PDF_UPLOADED": "PDF uploaded and embedded successfully.",
    "ANSWER_GENERATED": "Answer generated successfully.",
}

ERROR_MESSAGES = {
    "PDF_UPLOAD_FAILED": "Failed to upload PDF. Please check the file and try again.",
    "EMBEDDING_FAILED": "Failed to embed documents.",
    "ANSWER_GENERATION_FAILED": "Failed to generate answer. Please try again.",
    "INVALID_FILE": "Invalid file format. Please upload a PDF file.",
    "EMPTY_QUESTION": "Question cannot be empty.",
}

# File constraints
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {".pdf"}
