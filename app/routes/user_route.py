import hashlib
import random
import uuid

from flask import request, jsonify

from app import app, db
from app.models.user_model import User


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
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    my_referral = generate_referral_code()
    otp = generate_otp()

    new_user = User(
        packageID=package_id,
        name=name,
        email=email,
        password=hashed_password,
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


@app.route('/check_my_referral', methods=['GET'])
def check_my_referral():
    my_referral = request.args.get('myReferral')

    user = User.query.filter_by(myReferral=my_referral).first()
    if user:
        return jsonify({'message': 'User found', 'code': 200}), 200
    else:
        return jsonify({'message': 'User not found', 'code': 404}), 404



@app.route('/user_login', methods=['POST'])
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user.password == hashed_password:
            response_data = {
                'name': user.name,
                'email': user.email,
                'myReferral': user.myReferral,
                'friendReferral': user.friendReferral,
                'spotBalance': user.spotBalance,
                'fundingBalance': user.fundingBalance,
                'profit': user.profit,
                'RT': user.RT,
                'isVerify': user.isVerify,
                'OTP': user.OTP,
                'userID': user.userID,
                'message': 'Success',
                'code': 200
            }
            return jsonify(response_data), 200
        else:
            return jsonify({'message': 'Invalid credentials', 'code': 401}), 401
    else:
        return jsonify({'message': 'User not found', 'code': 404}), 404


# user update
@app.route('/user_update/<int:userID>', methods=['PUT'])
def user_update(userID):
    user = User.query.get(userID)

    if not user:
        return jsonify({'message': 'User not found', 'code': 404}), 404

    data = request.form

    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
        user.password = hashed_password
    if 'spotBalance' in data:
        user.spotBalance = float(data['spotBalance'])
    if 'fundingBalance' in data:
        user.fundingBalance = float(data['fundingBalance'])
    if 'profit' in data:
        user.profit = float(data['profit'])
    if 'RT' in data:
        user.RT = data['RT'] == 'true'
    if 'isVerify' in data:
        user.isVerify = data['isVerify'] == 'true'
    if 'OTP' in data:
        user.OTP = int(data['OTP'])

    db.session.commit()

    response_data = {
        'name': user.name,
        'email': user.email,
        'myReferral': user.myReferral,
        'friendReferral': user.friendReferral,
        'spotBalance': user.spotBalance,
        'fundingBalance': user.fundingBalance,
        'profit': user.profit,
        'RT': user.RT,
        'isVerify': user.isVerify,
        'OTP': user.OTP,
        'userID': user.userID,
        'message': 'Update Success',
        'code': 200
    }

    return jsonify(response_data), 200




@app.route('/search_user_by_id', methods=['GET'])
def search_user_by_id():
    user_id = request.form.get('userID')

    user = User.query.filter_by(userID=user_id).first()
    if user:
        response_data = {
            'name': user.name,
            'email': user.email,
            'myReferral': user.myReferral,
            'friendReferral': user.friendReferral,
            'spotBalance': user.spotBalance,
            'fundingBalance': user.fundingBalance,
            'profit': user.profit,
            'RT': user.RT,
            'isVerify': user.isVerify,
            'OTP': user.OTP,
            'userID': user.userID,
            'message': 'Found User',
            'code': 200
        }
        return jsonify(response_data), 200
    else:
        return jsonify({'message': 'User not found', 'code': 404}), 404
