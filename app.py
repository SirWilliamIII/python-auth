from flask import Flask, render_template, request, make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db
from routes.auth_routes import auth_bp
from routes.home_routes import home_bp

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)

@app.route('/')
def index():
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    accept_language = request.headers.get('Accept-Language')
    referer = request.headers.get('Referer', 'None')
    cookies = request.headers.get('Cookie', 'None')
    fingerprint = {
        'ip': client_ip,
        'user_agent': user_agent,
        'accept_language': accept_language,
        'referer': referer,
        'cookies': cookies,
    }
    response = make_response("Cookie is set")
    response.set_cookie('client_id', 'unique_id', max_age=30*24*60*60)
    print(response.get_data)
    print(f"Client fingerprint: {fingerprint}")

    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)