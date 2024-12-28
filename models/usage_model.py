from pymongo import MongoClient
from datetime import datetime, timedelta
from config import Config

class UsageModel:
    def __init__(self):
        client = MongoClient(Config.MONGO_URI)
        self.db = client.get_database('usage_monitoring')
        self.usage_collection = self.db['user_usage']
        
        # Create indexes for efficient querying
        self.usage_collection.create_index([('email', 1), ('date', -1)])

    def log_upload(self, email, file_name, file_size):
        today = datetime.combine(datetime.now().date(), datetime.min.time())
        current_time = datetime.now()
        
        # First, try to find an existing record
        existing_record = self.usage_collection.find_one({
            'email': email,
            'date': today
        })
        
        if not existing_record:
            # If no record exists, create a new one
            usage_record = self.usage_collection.find_one_and_update(
                {
                    'email': email,
                    'date': today
                },
                {
                    '$set': {
                        'email': email,
                        'date': today,
                        'total_upload_volume': file_size,
                        'upload_count': 1,
                        'uploads': [{
                            'file_name': file_name,
                            'file_size': file_size,
                            'timestamp': current_time
                        }],
                        'deletions': [],
                        'alert_stages': {
                            '80_percent_alert_sent': False,
                            'upload_blocked': False
                        }
                    }
                },
                upsert=True,
                return_document=True
            )
        else:
            # If record exists, update it
            usage_record = self.usage_collection.find_one_and_update(
                {
                    'email': email,
                    'date': today
                },
                {
                    '$inc': {
                        'total_upload_volume': file_size,
                        'upload_count': 1
                    },
                    '$push': {
                        'uploads': {
                            'file_name': file_name,
                            'file_size': file_size,
                            'timestamp': current_time
                        }
                    }
                },
                return_document=True
            )
        
        # Remove the '_id' field from the result before returning
        if usage_record and '_id' in usage_record:
            del usage_record['_id']
        return usage_record

    def log_deletion(self, email, file_name, file_size):
        today = datetime.combine(datetime.now().date(), datetime.min.time())
        current_time = datetime.now()
        
        # First, try to find an existing record
        existing_record = self.usage_collection.find_one({
            'email': email,
            'date': today
        })
        
        if not existing_record:
            # If no record exists, create a new one
            usage_record = self.usage_collection.find_one_and_update(
                {
                    'email': email,
                    'date': today
                },
                {
                    '$set': {
                        'email': email,
                        'date': today,
                        'total_upload_volume': 0,
                        'total_deletion_volume': file_size,
                        'upload_count': 0,
                        'deletion_count': 1,
                        'uploads': [],
                        'deletions': [{
                            'file_name': file_name,
                            'file_size': file_size,
                            'timestamp': current_time
                        }],
                        'alert_stages': {
                            '80_percent_alert_sent': False,
                            'upload_blocked': False
                        }
                    }
                },
                upsert=True,
                return_document=True
            )
        else:
            # If record exists, update it
            usage_record = self.usage_collection.find_one_and_update(
                {
                    'email': email,
                    'date': today
                },
                {
                    '$inc': {
                        'total_deletion_volume': file_size,
                        'deletion_count': 1
                    },
                    '$push': {
                        'deletions': {
                            'file_name': file_name,
                            'file_size': file_size,
                            'timestamp': current_time
                        }
                    }
                },
                return_document=True
            )
        
        deletion_record = {"email": email, 'file_deleted': file_name, "file_size": file_size, 'timestamp': current_time,
                        "date": today, "updated_deletion_volume": usage_record['total_deletion_volume'], "total_deletion_count": usage_record['deletion_count']}
        return deletion_record

    def check_daily_limit(self, email, file_size):
        today = datetime.combine(datetime.now().date(), datetime.min.time())
        current_usage = self.usage_collection.find_one({
            'email': email, 
            'date': today
        })
        
        if not current_usage:
            return True
        
        total_volume = current_usage.get('total_upload_volume', 0)
        return total_volume + file_size <= Config.DAILY_BANDWIDTH_LIMIT

    def reset_daily_usage(self):
        yesterday = datetime.combine((datetime.now().date() - timedelta(days=1)), datetime.min.time())
        self.usage_collection.delete_many({'date': yesterday})
        
    def get_daily_usage(self, email):
        today = datetime.combine(datetime.now().date(), datetime.min.time())
        usage_record = self.usage_collection.find_one({
            'email': email,
            'date': today
        })
        
        # Remove the '_id' field from the result before returning
        if usage_record and '_id' in usage_record:
            del usage_record['_id']
        return usage_record or {}
    
    def get_all_usage_records(self, email):
        """
        Retrieve all usage records for a user, sorted by date
        """
        usage_records = self.usage_collection.find({
            'email': email
        }).sort('date', -1)  # Sort by date ascending
        
        if not usage_records:
            return {}
        records = []
        for record in usage_records:
            if '_id' in record:
                del record['_id']
            records.append(record)
        
        return records