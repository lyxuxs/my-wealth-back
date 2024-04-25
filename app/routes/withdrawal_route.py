from datetime import date

from flask import jsonify, request

from app import app
from app import db
from app.models.transaction_model import Transaction
from app.models.user_model import User
from app.models.withdrawal_model import Withdrawal
from app.schemas import WithdrawalSchema

WITHDRAWAL_NETWORK = "PayPal"


@app.route('/add_withdrawal', methods=['POST'])
def add_withdrawal():
    try:

        amount = float(request.form.get('Amount'))
        user_id = int(request.form.get('UserID'))
        withdrawal_wallet_address = request.form.get('withdrawal_wallet_address')

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404

        withdrawal = Withdrawal(
            username=user.name,
            amount=amount,
            withdrawalWalletAddress=withdrawal_wallet_address,
            dateTime=datetime.utcnow(),
            status='Pending',
            withdrawalNetwork=WITHDRAWAL_NETWORK,
            userID=user_id
        )
        db.session.add(withdrawal)

        transaction = Transaction(
            username=user.name,
            amount=amount,
            dateTime=datetime.utcnow(),
            status='Pending',
            transactionType='Withdrawal',
            withdrawalID=withdrawal.withdrawalID,

            userID=user_id
        )
        db.session.add(transaction)

        db.session.commit()

        withdrawal_schema = WithdrawalSchema()
        withdrawal_data = withdrawal_schema.dump(withdrawal)

        response_data = {
            'username': withdrawal_data['username'],
            'Amount': withdrawal_data['amount'],
            'date&Time': withdrawal_data['dateTime'],
            'status': withdrawal_data['status'],
            'WithdrawalID': withdrawal_data['withdrawalID'],
            'UserID': withdrawal_data['userID'],
            'message': 'Withdrawal added successfully',
            'code': 'WITHDRAWAL_ADDED'
        }

        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/search_withdrawal', methods=['GET'])
def search_withdrawal_by_id():
    try:

        withdrawal_id = int(request.form.get('WithdrawalID'))

        withdrawal = Withdrawal.query.get(withdrawal_id)

        if not withdrawal:
            return jsonify({'message': 'Withdrawal not found', 'code': 'WITHDRAWAL_NOT_FOUND'}), 404

        withdrawal_data = {
            'WithdrawalID': withdrawal.withdrawalID,
            'Username': withdrawal.username,
            'Amount': withdrawal.amount,
            'DateTime': withdrawal.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
            'Status': withdrawal.status,
            'UserID': withdrawal.userID
        }

        return jsonify(withdrawal_data), 200
    except ValueError:
        return jsonify({'message': 'Invalid WithdrawalID format', 'code': 'INVALID_WITHDRAWAL_ID'}), 400
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/withdrawal_by_user_id', methods=['GET'])
def search_withdrawal_by_user():
    try:

        user_id = int(request.form.get('userID'))

        withdrawals = Withdrawal.query.filter_by(userID=user_id).all()

        if not withdrawals:
            return jsonify({'message': 'No withdrawals found for the user', 'code': 'NO_WITHDRAWALS_FOUND'}), 404

        withdrawal_data = []
        for withdrawal in withdrawals:
            withdrawal_info = {
                'WithdrawalID': withdrawal.withdrawalID,
                'Username': withdrawal.username,
                'Amount': withdrawal.amount,
                'DateTime': withdrawal.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Status': withdrawal.status,
                'UserID': withdrawal.userID
            }
            withdrawal_data.append(withdrawal_info)

        return jsonify(withdrawal_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/withdrawal_by_status', methods=['GET'])
def search_withdrawal_by_status():
    try:

        status = request.form.get('status')

        withdrawals = Withdrawal.query.filter_by(status=status).all()

        if not withdrawals:
            return jsonify(
                {'message': f'No withdrawals found with status {status}', 'code': 'NO_WITHDRAWALS_FOUND'}), 404

        withdrawal_data = []
        for withdrawal in withdrawals:
            withdrawal_info = {
                'WithdrawalID': withdrawal.withdrawalID,
                'Username': withdrawal.username,
                'Amount': withdrawal.amount,
                'DateTime': withdrawal.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Status': withdrawal.status,
                'UserID': withdrawal.userID
            }
            withdrawal_data.append(withdrawal_info)

        return jsonify(withdrawal_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/withdrawal_by_today', methods=['GET'])
def search_withdrawal_by_date_today():
    try:

        today = date.today()

        withdrawals = Withdrawal.query.filter(db.func.date(Withdrawal.dateTime) == today).all()

        if not withdrawals:
            return jsonify({'message': 'No withdrawals found for today', 'code': 'NO_WITHDRAWALS_FOUND'}), 404

        withdrawal_data = []
        for withdrawal in withdrawals:
            withdrawal_info = {
                'WithdrawalID': withdrawal.withdrawalID,
                'Username': withdrawal.username,
                'Amount': withdrawal.amount,
                'DateTime': withdrawal.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Status': withdrawal.status,
                'UserID': withdrawal.userID
            }
            withdrawal_data.append(withdrawal_info)

        return jsonify(withdrawal_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


from datetime import datetime, timedelta


@app.route('/withdrawal_by_week', methods=['GET'])
def search_withdrawal_by_date_week():
    try:

        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        withdrawals = Withdrawal.query.filter(
            Withdrawal.dateTime >= start_of_week,
            Withdrawal.dateTime <= end_of_week
        ).all()

        if not withdrawals:
            return jsonify({'message': 'No withdrawals found for this week', 'code': 'NO_WITHDRAWALS_FOUND'}), 404

        withdrawal_data = []
        for withdrawal in withdrawals:
            withdrawal_info = {
                'WithdrawalID': withdrawal.withdrawalID,
                'Username': withdrawal.username,
                'Amount': withdrawal.amount,
                'DateTime': withdrawal.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Status': withdrawal.status,
                'UserID': withdrawal.userID
            }
            withdrawal_data.append(withdrawal_info)

        return jsonify(withdrawal_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
