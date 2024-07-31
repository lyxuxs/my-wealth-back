from datetime import datetime, date, timedelta
from urllib.parse import urlencode
from flask import Flask, jsonify, request
from app import app, db
from app.models.deposit_model import Deposit
from app.models.transaction_model import Transaction
from app.models.user_model import User
from app.schemas import DepositSchema
from configparser import ConfigParser
import requests
import hmac
import hashlib
import time
import urllib.parse



from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


IPN_SECRET = '3o9QU1sHSLRvlXEVDyCmw2NaylOyfFoN'
PUBLIC_KEY = '27a1a686f619457d14844017aba64d454ad15cf64eef40c82a37e7efa3985729'
PRIVATE_KEY = '94E035c6F4ba4361C2deAa425b704Dd39f7c3aBa7275d8aF10eD6f96668e03b3'

def create_headers(payload):
    encoded_payload = urllib.parse.urlencode(payload)
    hmac_signature = hmac.new(
        PRIVATE_KEY.encode('utf-8'),
        encoded_payload.encode('utf-8'),
        hashlib.sha512
    ).hexdigest()
    headers = {
        'HMAC': hmac_signature
    }
    return headers

@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    data = request.json
    payload = {
        'version': 1,
        'key': PUBLIC_KEY,
        'cmd': 'create_transaction',
        'amount': data['amount'],
        'currency1': data['currency1'],
        'currency2': data['currency2'],
        'buyer_email': data['buyer_email'],
        'UserID': data['UserID'],
        'ipn_url': 'https://5.189.141.126:443/ipn',  # Set your public IPN URL
        'format': 'json'
    }
    headers = create_headers(payload)
    response = requests.post('https://www.coinpayments.net/api.php', data=payload, headers=headers)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to create transaction"}), response.status_code
    
    response_data = response.json()
    
    if response_data.get('error') != "ok":
        return jsonify({"error": response_data.get('error')}), 400
    
    return jsonify(response_data)

@app.route('/ipn', methods=['POST'])
def ipn():
    ipn_data = request.form.to_dict()

    hmac_signature = request.headers.get('HMAC')
    if not hmac_signature:
        return "HMAC signature missing", 400

    ipn_hmac = hmac.new(
        PRIVATE_KEY.encode('utf-8'),
        request.data,
        hashlib.sha512
    ).hexdigest()

    if hmac_signature != ipn_hmac:
        return "Invalid HMAC signature", 400

    # Process the IPN data
    print(ipn_data)  # Replace with your logic to handle the IPN data

    # return "IPN received", 200
    # //////////////////////////////////////////////////////////
    try:
        amount = float(ipn_data['Amount'])
        user_id = int(ipn_data['UserID'])

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404

        deposit = Deposit(
            username=user.name,
            amount=amount,
            dateTime=datetime.utcnow(),
            status='Pending',
            userID=user_id
        )
        db.session.add(deposit)
        db.session.commit()

        transaction = Transaction(
            username=user.name,
            amount=amount,
            dateTime=datetime.utcnow(),
            status='Pending',
            transactionType='Deposit',
            depositID=deposit.depositID,
            userID=user_id
        )
        db.session.add(transaction)
        db.session.commit()

        deposit_schema = DepositSchema()
        deposit_data = deposit_schema.dump(deposit)

        response_data = {
            'username': deposit_data['username'],
            'Amount': deposit_data['amount'],
            'date&Time': deposit_data['dateTime'],
            'status': deposit_data['status'],
            'DepositID': deposit_data['depositID'],
            'UserID': deposit_data['userID'],
            'message': 'Deposit added successfully',
            'code': 'DEPOSIT_ADDED'
        }

        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500

    # //////////////////////////////////////////////////////////

    

# @app.route('/testWallet', methods=['POST'])
# def testWallet():
#     parser = ConfigParser()
#     parser.read('config.ini')
#     API_KEY = parser.get('apikeys', 'API_KEY')
#     API_SECRET = parser.get('apikeys', 'API_SECRET')
#     IPN_URL = parser.get('apikeys', 'IPN_URL')
#
#     create_transaction_params = {
#         'amount': 10,
#         'currency1': 'USD',
#         'currency2': 'BTC',
#         'ipn_url': IPN_URL
#     }
#
#     transaction = coinpayments_api_call('create_transaction', create_transaction_params, API_KEY, API_SECRET)
#
#     if transaction['error'] == 'ok':
#         print(transaction['result']['amount'])
#         print(transaction['result']['address'])
#         txn_id = transaction['result']['txn_id']
#     else:
#         print(transaction['error'])
#         return jsonify({'message': transaction['error']}), 500
#
#     post_params1 = {
#         'txid': txn_id
#     }
#
#     transaction_info = coinpayments_api_call('get_tx_info', post_params1, API_KEY, API_SECRET)
#
#     if transaction_info['error'] == 'ok':
#         print(transaction_info['result']['amountf'])
#         print(transaction_info['result']['payment_address'])
#     else:
#         print(transaction_info['error'])
#
#     return jsonify({'message': 'Transaction tested successfully'}), 200
#
#
@app.route('/add_deposit', methods=['POST'])
def add_deposit():
    try:
        amount = float(request.form.get('Amount'))
        user_id = int(request.form.get('UserID'))

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404

        deposit = Deposit(
            username=user.name,
            amount=amount,
            dateTime=datetime.utcnow(),
            status='Pending',
            userID=user_id
        )
        db.session.add(deposit)
        db.session.commit()

        transaction = Transaction(
            username=user.name,
            amount=amount,
            dateTime=datetime.utcnow(),
            status='Pending',
            transactionType='Deposit',
            depositID=deposit.depositID,
            userID=user_id
        )
        db.session.add(transaction)
        db.session.commit()

        deposit_schema = DepositSchema()
        deposit_data = deposit_schema.dump(deposit)

        response_data = {
            'username': deposit_data['username'],
            'Amount': deposit_data['amount'],
            'date&Time': deposit_data['dateTime'],
            'status': deposit_data['status'],
            'DepositID': deposit_data['depositID'],
            'UserID': deposit_data['userID'],
            'message': 'Deposit added successfully',
            'code': 'DEPOSIT_ADDED'
        }

        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/search_deposit', methods=['GET'])
def search_deposit_by_id():
    try:
        deposit_id = int(request.args.get('depositID'))

        deposit = Deposit.query.get(deposit_id)

        if not deposit:
            return jsonify({'message': 'Deposit not found', 'code': 'DEPOSIT_NOT_FOUND'}), 404

        deposit_schema = DepositSchema()
        deposit_data = deposit_schema.dump(deposit)

        response_data = {
            'username': deposit_data['username'],
            'Amount': deposit_data['amount'],
            'date&Time': deposit_data['dateTime'],
            'status': deposit_data['status'],
            'DepositID': deposit_data['depositID'],
            'UserID': deposit_data['userID'],
            'message': 'Deposit details retrieved successfully',
            'code': 200
        }

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/deposit_by_user_id', methods=['GET'])
def search_deposits_by_user_id():
    try:
        user_id = int(request.args.get('UserID'))

        deposits = Deposit.query.filter_by(userID=user_id).all()

        if not deposits:
            return jsonify({'message': 'No deposits found for the user', 'code': 'NO_DEPOSITS_FOUND'}), 404

        deposit_data = []
        for deposit in deposits:
            deposit_info = {
                'date&Time': deposit.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Amount': deposit.amount,
                'status': deposit.status,
                'DepositID': deposit.depositID,
                'UserID': deposit.userID,
                'UserName': deposit.username,
            }
            deposit_data.append(deposit_info)

        return jsonify(deposit_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/search_deposit_by_status', methods=['GET'])
def search_deposits_by_status():
    try:
        status = str(request.args.get('status'))

        deposits = Deposit.query.filter_by(status=status).all()

        if not deposits:
            return jsonify({'message': 'No deposits found with the given status', 'code': 'NO_DEPOSITS_FOUND'}), 404

        deposit_data = []
        for deposit in deposits:
            deposit_info = {
                'date&Time': deposit.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Amount': deposit.amount,
                'status': deposit.status,
                'DepositID': deposit.depositID,
                'UserID': deposit.userID,
                'UserName': deposit.username,
            }
            deposit_data.append(deposit_info)

        return jsonify(deposit_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/search_deposit_today', methods=['GET'])
def search_deposit_today():
    try:
        today = date.today()

        deposits = Deposit.query.filter(db.func.date(Deposit.dateTime) == today).all()

        if not deposits:
            return jsonify({'message': 'No deposits found for today', 'code': 'NO_DEPOSITS_FOUND'}), 404

        deposit_schema = DepositSchema(many=True)
        deposit_data = deposit_schema.dump(deposits)

        return jsonify(deposit_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/search_deposit_week', methods=['GET'])
def search_deposit_week():
    try:
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        deposits = Deposit.query.filter(Deposit.dateTime >= start_of_week, Deposit.dateTime <= end_of_week).all()

        if not deposits:
            return jsonify({'message': 'No deposits found for this week', 'code': 'NO_DEPOSITS_FOUND'}), 404

        deposit_schema = DepositSchema(many=True)
        deposit_data = deposit_schema.dump(deposits)

        return jsonify(deposit_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/search_deposit_month', methods=['GET'])
def search_deposit_by_month():
    try:
        current_month = datetime.now().month
        current_year = datetime.now().year

        deposits = Deposit.query.filter(db.extract('month', Deposit.dateTime) == current_month) \
            .filter(db.extract('year', Deposit.dateTime) == current_year).all()

        if not deposits:
            return jsonify({'message': 'No deposits found for the current month', 'code': 'NO_DEPOSITS_FOUND'}), 404

        deposit_data = []
        for deposit in deposits:
            deposit_info = {
                'date&Time': deposit.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Amount': deposit.amount,
                'status': deposit.status,
                'DepositID': deposit.depositID,
                'UserID': deposit.userID,
                'UserName': deposit.username,
            }
            deposit_data.append(deposit_info)

        return jsonify(deposit_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/search_deposit_custom', methods=['GET'])
def search_deposit_by_custom_date():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

        deposits = Deposit.query.filter(Deposit.dateTime.between(start_datetime, end_datetime)).all()

        if not deposits:
            return jsonify(
                {'message': 'No deposits found for the specified date range', 'code': 'NO_DEPOSITS_FOUND'}), 404

        deposit_data = []
        for deposit in deposits:
            deposit_info = {
                'date&Time': deposit.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Amount': deposit.amount,
                'status': deposit.status,
                'DepositID': deposit.depositID,
                'UserID': deposit.userID,
                'UserName': deposit.username,
            }
            deposit_data.append(deposit_info)

        return jsonify(deposit_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/get_all_deposits', methods=['GET'])
def get_all_deposits():
    try:
        deposits = Deposit.query.all()

        deposit_data = []
        for deposit in deposits:
            deposit_info = {
                'DepositID': deposit.depositID,
                'UserID': deposit.userID,
                'UserName': deposit.username,
                'Amount': deposit.amount,
                'dateTime': deposit.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Status': deposit.status
            }
            deposit_data.append(deposit_info)

        return jsonify(deposit_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/update_deposit_status', methods=['PUT'])
def update_deposit_status():
    try:
        deposit_id = int(request.form.get('DepositID'))
        status = str(request.form.get('status'))

        deposit = Deposit.query.get(deposit_id)
        if not deposit:
            return jsonify({'message': 'Deposit not found', 'code': 'DEPOSIT_NOT_FOUND'}), 404

        deposit.status = status

        transaction = Transaction.query.filter_by(depositID=deposit_id).first()
        if transaction:
            transaction.status = status

        if status == 'Approved':
            user = User.query.get(deposit.userID)
            if not user:
                return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
            user.fundingBalance += deposit.amount

        db.session.commit()

        return jsonify({'message': 'Deposit status updated successfully', 'code': 'DEPOSIT_STATUS_UPDATED'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500