from models.usage_model import UsageModel
from config import Config

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
    
    def log_upload(self, user_id, file_size, file_name):
        # Added file_name parameter
        usage_record = self.usage_model.log_upload(user_id, file_size, file_name)
        return usage_record
    
    def check_usage_alerts(self, user_id):
        """
        Check if user is approaching daily bandwidth limit
        Generate alerts at 80% consumption
        """
        usage_record = self.usage_model.get_daily_usage(user_id)
        total_used = usage_record.get('total_upload_volume', 0)
        limit = Config.DAILY_BANDWIDTH_LIMIT
        
        return {
            'total_used': total_used,
            'limit': limit,
            'percentage_used': (total_used / limit) * 100,
            'alerts': {
                'approaching_limit': total_used >= (limit * 0.8),
                'limit_exceeded': total_used >= limit
            }
        }
    
    def log_deletion(self, user_id, file_size, file_name):
        """
        Log file deletion and update usage records
        """
        # Added file_name parameter
        return self.usage_model.log_deletion(user_id, file_size, file_name)

    def reset_daily_usage(self, user_id):
        """
        Reset daily usage for a specific user
        """
        return self.usage_model.reset_daily_usage(user_id)

    def get_daily_usage(self, user_id):
        """
        Provide comprehensive bandwidth consumption details
        """
        usage_record = self.usage_model.get_daily_usage(user_id)
        total_used = usage_record.get('total_upload_volume', 0)
        total_deleted = usage_record.get('total_deletion_volume', 0)
        limit = Config.DAILY_BANDWIDTH_LIMIT
        
        return {
            'user_id': usage_record.get('user_id'),
            'date': usage_record.get('date'),
            'total_limit': limit,
            'total_used': total_used,
            'total_deleted': total_deleted,
            'remaining': limit - total_used,
            'percentage_consumed': (total_used / limit) * 100,
            'upload_count': usage_record.get('upload_count', 0),
            'deletion_count': usage_record.get('deletion_count', 0),
            'uploads': usage_record.get('uploads', []),
            'deletions': usage_record.get('deletions', [])
        }
    
    def get_total_usage(self, user_id):
        """
        Get total usage including uploads and deletions history
        """
        return self.usage_model.get_total_usage(user_id)