from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET'])
@jwt_required(locations=["cookies"])
def home():
    curr_user = get_jwt_identity()
    return jsonify({'message': f'welcome to the home page, {curr_user["username"]}'}), 200

@home_bp.route('/debug', methods=['GET'])
def debug_cookies():
    print(request.cookies)
    return jsonify({'cookies': request.cookies}), 200