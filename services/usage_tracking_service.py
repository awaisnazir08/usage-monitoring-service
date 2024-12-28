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
            'bandwidth_percentage_used': (total_used / limit) * 100,
            'bandwidth_checks': {
                'bandwidth_limit_approaching': total_used >= (limit * 0.8),
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
            'total_bandwidth_limit': limit,
            'total_data_bandwidth_used': total_used,
            'total_volume_deleted': total_deleted,
            'remaining_bandwidth': limit - total_used,
            'bandwidth_percentage_consumed': (total_used / limit) * 100,
            'upload_count': usage_record.get('upload_count', 0),
            'deletion_count': usage_record.get('deletion_count', 0),
            'uploads': usage_record.get('uploads', []),
            'deletions': usage_record.get('deletions', [])
        }
    
    
    def get_complete_usage_stats(self, email):
        """
        Provide both daily usage records and overall summary statistics for a user
        
        Args:
            email (str): User's email address
        
        Returns:
            dict: Contains daily records and overall summary statistics
        """
        # Get all daily records
        daily_records = []
        total_used = 0
        total_deleted = 0
        total_upload_count = 0
        total_deletion_count = 0
        
        usage_records = self.usage_model.get_all_usage_records(email)
        
        for record in usage_records:
            if '_id' in record:
                del record['_id']
                
            # Calculate daily statistics
            daily_used = record.get('total_upload_volume', 0)
            daily_deleted = record.get('total_deletion_volume', 0)
            daily_limit = Config.DAILY_BANDWIDTH_LIMIT
            
            daily_stats = {
                'email': record.get('email'),
                'date': record.get('date'),
                'total_bandwidth_limit': daily_limit,
                'total_data_bandwidth_used': daily_used,
                'total_volume_deleted': daily_deleted,
                'remaining_bandwidth': daily_limit - daily_used,
                'bandwidth_percentage_consumed': (daily_used / daily_limit) * 100 if daily_limit else 0,
                'upload_count': record.get('upload_count', 0),
                'deletion_count': record.get('deletion_count', 0),
                'uploads': record.get('uploads', []),
                'deletions': record.get('deletions', [])
            }
            
            daily_records.append(daily_stats)
            
            # Accumulate totals for summary
            total_used += daily_used
            total_deleted += daily_deleted
            total_upload_count += record.get('upload_count', 0)
            total_deletion_count += record.get('deletion_count', 0)
        
        # Calculate actual date range and total days
        if daily_records:
            start_date = daily_records[-1]['date']
            end_date = daily_records[0]['date']
            # Calculate total days including days with no activity
            total_days = (end_date - start_date).days + 1
            print(total_days)
        else:
            start_date = None
            end_date = None
            total_days = 0
        
        # Calculate total limit based on actual date range
        total_limit = Config.DAILY_BANDWIDTH_LIMIT * total_days if total_days else 0
        
        # Calculate days with activity
        active_days = len(daily_records)
        
        return {
            'email': email,
            'summary_statistics': {
                'date_range': {
                    'start': start_date,
                    'end': end_date,
                    'total_days': total_days,
                    'days_with_activity': active_days,
                    'days_without_activity': total_days - active_days if total_days else 0
                },
                'bandwidth_totals': {
                    'total_bandwidth_provided': total_limit,
                    'total_data_bandwidth_used': total_used,
                    'total_volume_deleted': total_deleted,
                    'overall_bandwidth_percentage_consumed': (total_used / total_limit * 100) if total_limit else 0
                },
                'daily_averages': {
                    'average_daily_usage': total_used / total_days if total_days else 0,
                    'average_daily_deletions': total_deleted / total_days if total_days else 0,
                    'average_daily_upload_count': total_upload_count / total_days if total_days else 0,
                    'average_daily_deletion_count': total_deletion_count / total_days if total_days else 0,
                    'average_usage_on_active_days': total_used / active_days if active_days else 0,
                    'average_deletions_on_active_days': total_deleted / active_days if active_days else 0
                },
                'activity_totals': {
                    'total_upload_count': total_upload_count,
                    'total_deletion_count': total_deletion_count
                }
            },
            'daily_records': daily_records
        }