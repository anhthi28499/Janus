import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://janus:janus_pass@localhost:5432/janus_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_ENV = os.getenv('PINECONE_ENV')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
