import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
db = SQLAlchemy(app)
# CORS(app, resources={r"/appUsers": {"origins": "https://acard1990.github.io"}})

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/appUsers', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_info = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        user_list.append(user_info)
    return jsonify(user_list)

@app.route('/appUsers', methods=['POST'])
def add_user():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    new_user = User(first_name=first_name, last_name=last_name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully"})

@app.route('/appUsers/update/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if user:
        data = request.get_json()
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')
        db.session.commit()
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"error": "User not found"})

@app.route('/appUsers/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"error": "User not found"})

port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='0.0.0.0', port=port)