# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User  # ✅ IMPORT db and User FROM models.py

app = Flask(__name__)
CORS(app)

# ✅ Configure your PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mototracedb_owner:npg_AlMz7rkO0oYR@ep-lively-river-a58up56x-pooler.us-east-2.aws.neon.tech/mototracedb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Initialize the db with this app
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = generate_password_hash(data['password'])

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(port=3000, debug=True)
