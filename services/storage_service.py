import requests
from config import Config

class StorageService:
    @staticmethod
    def get_storage_status(token):
        try:
            response = requests.get(
                f"{Config.STORAGE_SERVICE_URL}/storage-status",
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            return None