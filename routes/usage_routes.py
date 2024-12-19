from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.usage_tracking_service import UsageTrackingService
from services.storage_service import StorageService

usage_bp = Blueprint('usage', __name__)
usage_service = UsageTrackingService()

@usage_bp.route('/api/usage/check-upload-bandwidth', methods=['POST'])
@AuthService.token_required
def check_upload_bandwidth(user):
    data = request.json
    # print(data)
    file_size = data.get('file_size', 0)
    # print(user)
    result = usage_service.check_upload_bandwidth(user['email'], file_size)
    
    return jsonify(result), 200 if result['allowed'] else 400

@usage_bp.route('/api/usage/log-upload', methods=['POST'])
@AuthService.token_required
def log_upload(user):
    data = request.json
    file_name = data.get('file_name', '')
    file_size = data.get('file_size', 0)
    
    usage_record = usage_service.log_upload(user['email'], file_name, file_size)
    
    return jsonify(usage_record), 200 if usage_record else 400

@usage_bp.route('/api/usage/check-usage-alerts', methods = ['GET'])
@AuthService.token_required
def check_alert_required_or_not(user):
    
    alert_logs = usage_service.check_usage_alerts(user['email'])
    
    return jsonify(alert_logs), 200 if alert_logs else 400

@usage_bp.route('/api/usage/daily-summary', methods=['GET'])
@AuthService.token_required
def get_daily_summary(user):
    usage = usage_service.get_daily_usage(user['email'])
    return jsonify(usage), 200

@usage_bp.route('/api/usage/log-deletion', methods=['POST'])
@AuthService.token_required
def log_deletion(user):
    """
    Log video file deletion and update usage statistics
    """
    data = request.json
    file_name = data.get('file_name', "")
    file_size = data.get('file_size', 0)
    
    deletion_record = usage_service.log_deletion(user['email'], file_name, file_size)
    
    return jsonify(deletion_record), 200 if deletion_record else 400

@usage_bp.route('/api/usage/reset-daily', methods=['POST'])
@AuthService.token_required
def reset_daily_usage(user):
    """
    Manually reset daily usage (typically for admin or system use)
    """
    result = usage_service.reset_daily_usage(user['email'])
    return jsonify(result), 200