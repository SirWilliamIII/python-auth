from flask import Blueprint, request, jsonify, make_response, redirect
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models.user import User
from models import db

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'username and password are required.'}, 400)
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'user registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'username already exists or registration failed, {e}'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity={'id': user.id, 'username': user.username})
        response = jsonify({'message': 'login successful'})
        response.set_cookie(key='access_token_cookie', value=token, httponly=True, secure=True)
        response = make_response(redirect('/home'))
        return response
    return jsonify({'error': 'invalid username or password'})

