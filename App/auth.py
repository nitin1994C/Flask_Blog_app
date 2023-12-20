from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request format"}), 400

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return jsonify({"message": "Logged in successfully", "user_id": user.id}), 200
        else:
            return jsonify({"error": "Incorrect password. Please try again"}), 401
    else:
        return jsonify({"error": "Email does not exist. Please sign up"}), 404

#SIGNUP
    
@auth.route("/sign-up", methods=['POST'])
def sign_up():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request format"}), 400

    email = data.get("email")
    username = data.get("username")
    password1 = data.get("password1")
    password2 = data.get("password2")

    email_exists = User.query.filter_by(email=email).first()
    username_exists = User.query.filter_by(username=username).first()

    if email_exists:
        return jsonify({"error": "Email is already in use. Please choose another one"}), 409
    elif username_exists:
        return jsonify({"error": "Username is already taken. Please choose another one"}), 409
    elif password1 != password2:
        return jsonify({"error": "Passwords do not match. Please try again"}), 400
    elif len(username) < 2:
        return jsonify({"error": "Username is too short. Please choose a longer one"}), 400
    elif len(password1) < 6:
        return jsonify({"error": "Password is too short. Please choose a longer one"}), 400
    elif len(email) < 4:
        return jsonify({"error": "Email is invalid. Please provide a valid email address"}), 400
    else:
        new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return jsonify({"message": "Account created successfully", "user_id": new_user.id}), 201

# logout route
    
@auth.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
