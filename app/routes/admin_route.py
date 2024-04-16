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
    data = request.json
    user_name = data.get('user_name')
    email = data.get('email')
    password = data.get('password')

    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({'message': 'Admin already exists with the given email', 'code': 400}), 400

    otp = generate_otp()
    new_admin = Admin(user_name=user_name, email=email, password=password, otp=otp)
    db.session.add(new_admin)
    db.session.commit()

    send_otp_email('dinethpanditha9@gmail.com', otp, user_name)

    new_admin.otp = otp
    db.session.commit()

    return jsonify({'message': 'Admin created successfully', 'code': 201}), 201
