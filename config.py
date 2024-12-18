import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')
    STORAGE_SERVICE_URL = os.getenv('STORAGE_SERVICE_URL')
    DAILY_BANDWIDTH_LIMIT = int(os.getenv('DAILY_BANDWIDTH_LIMIT', 104857600))