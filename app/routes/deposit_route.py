from datetime import datetime, date, timedelta

from flask import jsonify, request

from app import app
from app import db
from app.models.deposit_model import Deposit
from app.models.transaction_model import Transaction
from app.models.user_model import User
from app.schemas import DepositSchema


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
        deposit_id = int(request.form.get('depositID'))

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

        user_id = int(request.form.get('UserID'))

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

        status = str(request.form.get('status'))

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

        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

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
