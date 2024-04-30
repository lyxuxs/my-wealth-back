import hashlib
import random
import uuid

from flask import request, jsonify
from flask_mail import Message

from app import app, db
from app.models.mainRef_model import MainRef
from app.models.secondRef_model import SecondRef
from app.models.thirdRef_model import ThirdRef
from app.models.user_model import User
from app.routes.admin_route import mail


def send_otp_email(email, otp):
    msg = Message('New User Registration OTP', recipients=[email])
    msg.body = f'Hello, your registration OTP is: {otp}'
    mail.send(msg)


def generate_referral_code():
    return str(uuid.uuid4().hex)[:6]


def generate_otp():
    return random.randint(1000, 9999)


def add_to_third_ref(user_id, my_referral):
    third_ref = ThirdRef(
        userID=user_id,
        Ref=my_referral
    )
    db.session.add(third_ref)
    db.session.commit()
    return third_ref


def add_to_second_ref(user_id, ref_tree_id, friend_referral):
    second_ref = SecondRef(
        refTreeID=ref_tree_id,
        userID=user_id,
        Ref=friend_referral
    )
    db.session.add(second_ref)
    db.session.commit()
    return second_ref


def add_to_main_ref(user_id, ref_tree_id, friend_referral):
    main_ref = MainRef(
        refTreeID=ref_tree_id,
        userID=user_id,
        Ref=friend_referral
    )
    db.session.add(main_ref)
    db.session.commit()
    return main_ref


@app.route('/user_register', methods=['POST'])
def user_register():
    referral = request.form.get('friendReferral')

    friend_user = User.query.filter_by(myReferral=referral).first()
    if friend_user:
        package_id = request.form.get('packageID')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        my_referral = generate_referral_code()
        otp = generate_otp()
        encrypted_otp = hashlib.sha256(str(otp).encode()).hexdigest()

        new_user = User(
            packageID=package_id,
            name=name,
            email=email,
            password=hashed_password,
            myReferral=my_referral,
            friendReferral=referral,
            spotBalance=0,
            fundingBalance=0,
            profit=0,
            RT=False,
            isVerify=False,
            OTP=encrypted_otp
        )

        db.session.add(new_user)
        db.session.commit()

        user_id = new_user.userID

        third_ref = add_to_third_ref(user_id, my_referral)

        friend_user_second_ref = SecondRef.query.filter_by(userID=friend_user.userID).first()
        if friend_user_second_ref:
            second_ref = add_to_second_ref(user_id, third_ref.refTreeID, friend_user.friendReferral)

            friend_user_main_ref = MainRef.query.filter_by(userID=friend_user.userID).first()
            if friend_user_main_ref:
                add_to_main_ref(user_id, second_ref.refTreeID, friend_user.friendReferral)

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
            'userID': new_user.userID,
            'message': 'Success',
            'code': 200
        }

        return jsonify(response_data), 200
    else:
        return jsonify({'message': 'Friend referral not found', 'code': 404}), 404




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

    if not user:
        return jsonify({'message': 'User Email not found', 'code': 404}), 404

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user.password != hashed_password:
        return jsonify({'message': 'Invalid credentials', 'code': 401}), 401

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
        'userID': user.userID,
        'message': 'Success',
        'code': 200
    }
    return jsonify(response_data), 200


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
        hashed_otp = hashlib.sha256(data['OTP'].encode()).hexdigest()
        user.OTP = hashed_otp

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


@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'name': user.name,
            'email': user.email,
            'myReferral': user.myReferral,
            'friendReferral': user.friendReferral,
            'spotBalance': user.spotBalance,
            'fundingBalance': user.fundingBalance,
            'profit': user.profit,
            'RT': user.RT,
            'isVerify': user.isVerify,
            'userID': user.userID
        }
        user_list.append(user_data)

    response_data = {
        'users': user_list
    }
    return jsonify(response_data)


@app.route('/all_funding_balance', methods=['GET'])
def get_all_users_funding_balance():
    users = User.query.all()
    total_funding_balance = sum(user.fundingBalance for user in users)

    response_data = {
        'Total Funding Balance': total_funding_balance
    }
    return jsonify(response_data)


@app.route('/users_spot_balance', methods=['GET'])
def get_all_users_spot_balance():
    total_spot_balance = sum(user.spotBalance for user in User.query.all())

    response_data = {
        'total_spot_balance': total_spot_balance
    }

    return jsonify(response_data)


@app.route('/users_total_balance', methods=['GET'])
def get_all_users_total_balance():
    total_spot_balance = sum(user.spotBalance for user in User.query.all())
    total_funding_balance = sum(user.fundingBalance for user in User.query.all())
    total_balance = total_spot_balance + total_funding_balance

    response_data = {
        'total_balance': total_balance
    }

    return jsonify(response_data)


@app.route('/rt_funding_balance', methods=['GET'])
def get_all_rt_users_funding_balance():
    rt_users = User.query.filter_by(RT=True).all()
    total_funding_balance = sum(user.fundingBalance for user in rt_users)

    response_data = {
        'Total_RT_Funding_Balance': total_funding_balance
    }

    return jsonify(response_data)


@app.route('/rt_users_spot_balance', methods=['GET'])
def get_all_rt_users_spot_balance():
    rt_users = User.query.filter_by(RT=True).all()
    total_spot_balance = sum(user.spotBalance for user in rt_users)

    response_data = {
        'total_spot_balance': total_spot_balance
    }

    return jsonify(response_data)


@app.route('/all_rt_users_balance', methods=['GET'])
def get_all_rt_users_balance():
    rt_users = User.query.filter_by(RT=True).all()

    total_spot_balance = sum(user.spotBalance for user in rt_users)
    total_funding_balance = sum(user.fundingBalance for user in rt_users)
    total_balance = total_spot_balance + total_funding_balance

    response_data = {
        'total_balance': total_balance
    }

    return jsonify(response_data)


@app.route('/send_otp', methods=['POST'])
def send_otp():
    user_id = request.form.get('userID')
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found', 'code': 404}), 404

    otp = generate_otp()

    encrypted_otp = hashlib.sha256(str(otp).encode()).hexdigest()

    user.OTP = encrypted_otp
    db.session.commit()

    send_otp_email(user.email, otp)

    response_data = {
        'message': 'OTP sent',
        'code': 200
    }

    return jsonify(response_data), 200


@app.route('/check_user_OTP', methods=['GET'])
def check_user_otp():
    user_id = request.form.get('userID')
    otp_entered = request.form.get('OTP')

    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found', 'code': 404}), 404

    decrypted_stored_otp = user.OTP

    encrypted_entered_otp = hashlib.sha256(str(otp_entered).encode()).hexdigest()

    if decrypted_stored_otp == encrypted_entered_otp:
        user.isVerify = True
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
            'isVerify': True,
            'userID': user.userID,
            'message': 'OTP verified successfully',
            'code': 200
        }

        return jsonify(response_data), 200
    else:
        return jsonify({'message': 'Invalid OTP', 'code': 401}), 401
