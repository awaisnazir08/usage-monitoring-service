from pymongo import MongoClient
from datetime import datetime, timedelta
from config import Config

class UsageModel:
    def __init__(self):
        client = MongoClient(Config.MONGO_URI)
        self.db = client.get_database('usage_monitoring')
        self.usage_collection = self.db['user_usage']
        
        # Create indexes for efficient querying
        self.usage_collection.create_index([('user_id', 1), ('date', -1)])

    def log_upload(self, user_id, file_size):
        today = datetime.now().date()
        
        # Find or create daily usage record
        usage_record = self.usage_collection.find_one_and_update(
            {
                'user_id': user_id, 
                'date': today
            },
            {
                '$setOnInsert': {
                    'user_id': user_id,
                    'date': today,
                    'total_upload_volume': 0,
                    'upload_count': 0,
                    'alert_stages': {
                        '80_percent_alert_sent': False,
                        'upload_blocked': False
                    }
                },
                '$inc': {
                    'total_upload_volume': file_size,
                    'upload_count': 1
                }
            },
            upsert=True,
            return_document=True
        )
        
        return usage_record

    def check_daily_limit(self, user_id, file_size):
        today = datetime.now().date()
        current_usage = self.usage_collection.find_one({
            'user_id': user_id, 
            'date': today
        })
        
        if not current_usage:
            return True
        
        total_volume = current_usage.get('total_upload_volume', 0)
        return total_volume + file_size <= Config.DAILY_BANDWIDTH_LIMIT

    def reset_daily_usage(self):
        yesterday = datetime.now().date() - timedelta(days=1)
        self.usage_collection.delete_many({'date': yesterday})