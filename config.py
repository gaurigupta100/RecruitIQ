import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "resume-screening-secret-key-2026")

DATABASE_PATH = os.path.join(BASE_DIR, "database", "database.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MODELS_FOLDER = os.path.join(BASE_DIR, "models")

ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

CLASSIFIER_PATH = os.path.join(MODELS_FOLDER, "resume_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODELS_FOLDER, "tfidf_vectorizer.pkl")
LABEL_ENCODER_PATH = os.path.join(MODELS_FOLDER, "label_encoder.pkl")
