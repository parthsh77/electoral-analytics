import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///electoral.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False