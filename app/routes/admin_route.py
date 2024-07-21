from random import randint

from flask import jsonify, request
from flask_mail import Mail, Message

from app import app
from app import db
from app.models.admin_model import Admin

mail = Mail(app)


def generate_otp():
    return randint(1000, 9999)


def send_otp_email(email, otp, user_name):
    msg = Message('New Admin Registration OTP', recipients=[email])
    msg.body = f'Hello {user_name}, your registration OTP is: {otp}'
    mail.send(msg)


@app.route('/admin_register', methods=['POST'])
def create_admin():
    SEND_OTP_EMAIL = 'linifernando123@gmail.com'
    user_name = request.json.get('user_name')
    email = request.json.get('email')
    password = request.json.get('password')

    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({'message': 'Admin already exists with the given email', 'code': 400}), 400

    otp = generate_otp()
    new_admin = Admin(user_name=user_name, email=email, password=password, otp=otp)
    db.session.add(new_admin)
    db.session.commit()

    send_otp_email(SEND_OTP_EMAIL, otp, user_name)

    new_admin.otp = otp
    db.session.commit()

    return jsonify({'message': 'Admin created successfully', 'code': 201}), 201


@app.route('/check_otp', methods=['POST'])
def check_otp():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')

    admin = Admin.query.filter_by(email=email).first()
    if not admin:
        return jsonify({'message': 'Admin not found with the given email', 'code': 404}), 404

    if otp != admin.otp:
        return jsonify({'message': 'Invalid OTP', 'code': 400}), 400

    admin.is_verified = True
    db.session.commit()

    return jsonify({'message': 'OTP verified successfully', 'code': 200}), 200


@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.json.get('email')
    password = request.json.get('password')

    admin = Admin.query.filter_by(email=email).first()

    if not admin:
        return jsonify({'message': 'Email not found', 'code': 404}), 404

    if admin.password != password:
        return jsonify({'message': 'Invalid  Password', 'code': 401}), 401

    response_data = {
        'user_id': admin.admin_id,
        'user_name': admin.user_name,
        'email': admin.email,
        'if_verify': admin.is_verified,

        'message': 'Login successful',
        'code': 200
    }

    return jsonify(response_data), 200


@app.route('/admin_delete/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    admin = Admin.query.get(admin_id)

    if not admin:
        return jsonify({'message': 'Admin not found with the given ID', 'code': 404}), 404

    db.session.delete(admin)
    db.session.commit()

    return jsonify({'message': 'Admin deleted successfully', 'code': 200}), 200
