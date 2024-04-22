import random
import uuid

from flask import jsonify, request
from flask_mail import Mail, Message

from app import app, db
from app.models.user_model import User

mail = Mail(app)


def send_otp_email(email, name, otp):
    msg = Message('User Registration OTP', recipients=[email])
    msg.body = f'Hello {name}, Your Registration OTP is: {otp}'
    mail.send(msg)


def generate_referral_code():
    return str(uuid.uuid4().hex)[:6]


def generate_otp():
    return random.randint(1000, 9999)


@app.route('/user_register', methods=['POST'])
def user_register():
    package_id = request.form.get('packageID')
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    friend_referral = request.form.get('friendReferral')

    my_referral = generate_referral_code()
    otp = generate_otp()

    send_otp_email(email, name, otp)
    new_user = User(
        packageID=package_id,
        name=name,
        email=email,
        password=password,
        myReferral=my_referral,
        friendReferral=friend_referral,
        spotBalance=0,
        fundingBalance=0,
        profit=0,
        RT=False,
        isVerify=False,
        OTP=otp
    )

    db.session.add(new_user)
    db.session.commit()

    response_data = {
        'name': new_user.name,
        'email': new_user.email,
        'myReferral': new_user.myReferral,
        'friendReferral': new_user.friendReferral,
        'spotBalance': new_user.spotBalance,
        'fundingBalance': new_user.fundingBalance,
        'profit': new_user.profit,
        'RT': new_user.RT,
        'isVerify': new_user.isVerify,
        'OTP': new_user.OTP,
        'userID': new_user.userID,
        'message': 'Success',
        'code': 200
    }

    return jsonify(response_data), 200


@app.route('/check_friend_referral', methods=['GET'])
def check_friend_referral():
    friend_referral = request.args.get('friendReferral')

    user = User.query.filter_by(friendReferral=friend_referral).first()
    if user:
        return jsonify({'message': 'User found', 'code': 200}), 200
    else:
        return jsonify({'message': 'User not found', 'code': 404}), 404

