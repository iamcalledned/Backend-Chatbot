from flask import Blueprint, request, jsonify
from models import UserInfo, AuthDetails
from extensions import db, bcrypt
from email_validator import validate_email, EmailNotValidError

# Blueprint setup
api = Blueprint('api', __name__)

@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Basic validation checks
    if not data or not data.get('user_id') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing data'}), 400

    # Email and UserID validation
    try:
        valid = validate_email(data['email'])
        email = valid.email
        user_id = data['user_id']
    except EmailNotValidError as e:
        return jsonify({'error': str(e)}), 400

    # Check if user or email already exists
    if UserInfo.query.filter_by(email=email).first() or UserInfo.query.filter_by(user_id=user_id).first():
        return jsonify({'error': 'User ID or Email already exists'}), 409

    # Create new UserInfo instance
    new_user_info = UserInfo(user_id=user_id, email=email)
    db.session.add(new_user_info)
    db.session.commit()  # Commit to get the system_id generated

    # Create new AuthDetails instance
    new_auth_details = AuthDetails(system_id=new_user_info.system_id)
    new_auth_details.set_password(data['password'])
    db.session.add(new_auth_details)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Basic validation checks
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing data'}), 400

    # Find user by email
    user_info = UserInfo.query.filter_by(email=data['email']).first()

    # If user is found and password matches
    if user_info and AuthDetails.query.filter_by(system_id=user_info.system_id).first().check_password(data['password']):
        # You can implement token generation or session creation here
        # For simplicity, just return a success message
        return jsonify({'message': 'Login successful', 'success': True}), 200

    # If authentication fails
    return jsonify({'error': 'Invalid credentials', 'success': False}), 401

