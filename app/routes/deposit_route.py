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


from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


IPN_SECRET = '3o9QU1sHSLRvlXEVDyCmw2NaylOyfFoN'

def get_callback_address():
    url = 'https://www.coinpayments.net/api.php'
    
    # Current UNIX timestamp
    nonce = str(int(time.time() * 1000))
    
    # Required parameters for the request
    params = {
        'version': '1',
        'cmd': 'get_callback_address',
        'key': API_KEY,
        'currency': "USD",
        'nonce': nonce
    }
    
    # Sort parameters and create the query string
    post_data = '&'.join([f'{k}={params[k]}' for k in sorted(params)])
    
    # Create the HMAC signature
    signature = hmac.new(
        IPN_SECRET.encode('utf-8'),
        post_data.encode('utf-8'),
        hashlib.sha512
    ).hexdigest()
    
    # Headers for the request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'HMAC': signature
    }
    
    # Make the request
    response = requests.post(url, data=post_data, headers=headers)
    
    # Print the response
    return response.json()

@app.route('/ipn', methods=['POST'])
def ipn():
    try:
        # Verify HMAC signature
        hmac_header = request.headers.get('HMAC')
        if not hmac_header:
            return jsonify({'status': 'error', 'message': 'No HMAC header'}), 400

        # Recreate the HMAC signature
        request_string = request.form.to_dict()
        encoded_data = urlencode(request_string)
        hmac_calculated = hmac.new(IPN_SECRET.encode('utf-8'), encoded_data.encode('utf-8'), hashlib.sha512).hexdigest()
        
        if hmac_header != hmac_calculated:
            print(f'Expected HMAC: {hmac_calculated}')
            print(f'Received HMAC: {hmac_header}')
            return jsonify({'status': 'error', 'message': 'Invalid HMAC signature'}), 400

        # Process IPN data
        print(f"Received IPN: {request_string}")

        # Perform your business logic here
        if request_string.get('status') == '100':
            # Payment confirmed
            print("Payment confirmed")
            # Perform your logic for a confirmed payment
        else:
            # Payment not confirmed
            print("Payment not confirmed")
            # Perform your logic for a non-confirmed payment

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print(f"Error processing IPN: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/ipn_handler', methods=['POST'])
def ipn_handler():
    try:
        # CoinPayments requires the IPN to be verified by using HMAC SHA512
        hmac_header = request.headers.get('HMAC')
        if not hmac_header:
            return jsonify({'error': 'Missing HMAC header'}), 400

        request_data = request.form.to_dict()
        api_secret = IPN_SECRET  # Use the same API secret as in your CoinPayments account

        # Create HMAC signature
        encoded_data = request.data
        hmac_calculated = hmac.new(api_secret.encode(), encoded_data, hashlib.sha512).hexdigest()

        # Verify HMAC signature
        if hmac_header != hmac_calculated:
            return jsonify({'error': 'Invalid HMAC signature'}), 400

        # Process the IPN data
        txn_id = request_data.get('txn_id')
        status = int(request_data.get('status'))
        amount = float(request_data.get('amount1'))
        currency = request_data.get('currency1')

        # Update your database based on the transaction status
        if status >= 100 or status == 2:  # Payment is complete or queued for nightly payout
            # Payment is complete
            # Update your database to mark the transaction as completed
            pass
        elif status < 0:
            # Payment is canceled or has failed
            # Update your database to mark the transaction as failed/canceled
            pass
        else:
            # Payment is pending
            # Update your database to mark the transaction as pending
            pass

        return jsonify({'message': 'IPN received successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def coinpayments_api_call(cmd, params, api_key, api_secret):
    params['cmd'] = cmd
    params['key'] = api_key
    params['format'] = 'json'

    post_url = 'https://www.coinpayments.net/api.php'
    post_data = '&'.join([f"{key}={value}" for key, value in params.items()])

    hmac_sign = hmac.new(api_secret.encode(), post_data.encode(), hashlib.sha512).hexdigest()
    headers = {'hmac': hmac_sign}

    response = requests.post(post_url, data=params, headers=headers)
    return response.json()


@app.route('/testWallet', methods=['POST'])
def testWallet():
    parser = ConfigParser()
    parser.read('config.ini')
    API_KEY = parser.get('apikeys', 'API_KEY')
    API_SECRET = parser.get('apikeys', 'API_SECRET')
    IPN_URL = parser.get('apikeys', 'IPN_URL')

    create_transaction_params = {
        'amount': 10,
        'currency1': 'USD',
        'currency2': 'BTC',
        'ipn_url': IPN_URL
    }

    transaction = coinpayments_api_call('create_transaction', create_transaction_params, API_KEY, API_SECRET)

    if transaction['error'] == 'ok':
        print(transaction['result']['amount'])
        print(transaction['result']['address'])
        txn_id = transaction['result']['txn_id']
    else:
        print(transaction['error'])
        return jsonify({'message': transaction['error']}), 500

    post_params1 = {
        'txid': txn_id
    }

    transaction_info = coinpayments_api_call('get_tx_info', post_params1, API_KEY, API_SECRET)

    if transaction_info['error'] == 'ok':
        print(transaction_info['result']['amountf'])
        print(transaction_info['result']['payment_address'])
    else:
        print(transaction_info['error'])

    return jsonify({'message': 'Transaction tested successfully'}), 200


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