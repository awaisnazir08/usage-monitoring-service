from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.usage_tracking_service import UsageTrackingService
from services.storage_service import StorageService

usage_bp = Blueprint('usage', __name__)
usage_service = UsageTrackingService()

@usage_bp.route('/api/usage/check-upload-bandwidth', methods=['GET'])
@AuthService.token_required
def check_upload_bandwidth(user):
    data = request.json
    file_size = data.get('file_size', 0)
    
    result = usage_service.check_upload_bandwidth(user['_id'], file_size)
    
    return jsonify(result), 200 if result['allowed'] else 400

@usage_bp.route('/api/usage/log-upload', methods=['POST'])
@AuthService.token_required
def log_upload(user):
    data = request.json
    file_size = data.get('file_size', 0)
    
    usage_record = usage_service.log_upload(user['_id'], file_size)
    
    return jsonify(usage_record), 200 if usage_record else 400

@usage_bp.route('/api/usage/daily-summary', methods=['GET'])
@AuthService.token_required
def get_daily_summary(user):
    usage = usage_service.get_daily_usage(user['_id'])
    return jsonify(usage), 200

@usage_bp.route('/api/usage/storage-status', methods=['GET'])
@AuthService.token_required
def get_storage_status(user):
    token = request.headers.get('Authorization').split(' ')[1]
    storage_status = StorageService.get_storage_status(token)
    
    if storage_status:
        return jsonify(storage_status), 200
    return jsonify({'error': 'Could not retrieve storage status'}), 500