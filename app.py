from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())



# Routes
@app.route('/register', methods=['POST'])
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
        return jsonify({'error': 'username already exists or registration failed'}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity={'id': user.id, 'username': user.username})
        return jsonify({'message': 'Login successful', 'token': token}), 200
    return jsonify({'error': 'invalid username or password'})


@app.route('/home', methods=['GET'])
@jwt_required()
def home():
    curr_user = get_jwt_identity()
    return jsonify({'message': f'welcome to the home page, {curr_user['username']}'}), 200


if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


