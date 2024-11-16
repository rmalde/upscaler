import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
