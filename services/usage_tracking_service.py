from models.usage_model import UsageModel
from config import Config

class UsageTrackingService:
    def __init__(self):
        self.usage_model = UsageModel()
    
    def check_upload_bandwidth(self, email, file_size):
        # Check if upload is allowed
        if not self.usage_model.check_daily_limit(email, file_size):
            return {
                'allowed': False,
                'message': 'Daily bandwidth limit exceeded'
            }
        
        return {
            'allowed': True,
            'message': 'Upload permitted'
        }
    
    def log_upload(self, email, file_name, file_size):
        # Added file_name parameter
        usage_record = self.usage_model.log_upload(email, file_name, file_size)
        return usage_record
    
    def check_usage_alerts(self, email):
        """
        Check if user is approaching daily bandwidth limit
        Generate alerts at 80% consumption
        """
        usage_record = self.usage_model.get_daily_usage(email)
        total_used = usage_record.get('total_upload_volume', 0)
        limit = Config.DAILY_BANDWIDTH_LIMIT
        
        return {
            'total_bandwidth_used': total_used,
            'bandwidth_total_limit': limit,
            'bandwith_percentage_used': (total_used / limit) * 100,
            'bandwidth_alerts': {
                'bandwidth_approaching_limit': total_used >= (limit * 0.8),
                'bandwidth_limit_exceeded': total_used >= limit
            }
        }
    
    def log_deletion(self, email, file_name, file_size):
        """
        Log file deletion and update usage records
        """
        # Added file_name parameter
        return self.usage_model.log_deletion(email, file_name, file_size)

    def reset_daily_usage(self, email):
        """
        Reset daily usage for a specific user
        """
        return self.usage_model.reset_daily_usage(email)

    def get_daily_usage(self, email):
        """
        Provide comprehensive bandwidth consumption details
        """
        usage_record = self.usage_model.get_daily_usage(email)
        total_used = usage_record.get('total_upload_volume', 0)
        total_deleted = usage_record.get('total_deletion_volume', 0)
        limit = Config.DAILY_BANDWIDTH_LIMIT
        
        return {
            'email': usage_record.get('email'),
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