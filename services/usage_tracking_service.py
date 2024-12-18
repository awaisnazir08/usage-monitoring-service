from models.usage_model import UsageModel
from config import Config
from datetime import datetime

class UsageTrackingService:
    def __init__(self):
        self.usage_model = UsageModel()

    def check_upload_bandwidth(self, user_id, file_size):
        # Check if upload is allowed
        if not self.usage_model.check_daily_limit(user_id, file_size):
            return {
                'allowed': False,
                'message': 'Daily bandwidth limit exceeded'
            }
        
        return {
            'allowed': True,
            'message': 'Upload permitted'
        }
    
    def log_upload(self, user_id, file_size):
        usage_record = self.usage_model.log_upload(user_id, file_size)
        return usage_record

    def get_daily_usage(self, user_id):
        # Retrieve daily usage for a user
        today = datetime.now().date()
        usage_record = self.usage_model.usage_collection.find_one({
            'user_id': user_id,
            'date': today
        })
        
        return usage_record or {}