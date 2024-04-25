from datetime import date, datetime, timedelta

from flask import jsonify, request

from app import app, db
from app.models.transaction_model import Transaction


@app.route('/search_transaction', methods=['GET'])
def search_transaction_by_id():
    try:

        transaction_id = int(request.form.get('TransactionID'))

        transaction = Transaction.query.get(transaction_id)

        if not transaction:
            return jsonify({'message': 'Transaction not found', 'code': 'TRANSACTION_NOT_FOUND'}), 404

        transaction_data = {
            'TransactionID': transaction.transactionID,
            'Username': transaction.username,
            'Amount': transaction.amount,
            'DateTime': transaction.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
            'TransactionType': transaction.transactionType,
            'Status': transaction.status,
            'UserID': transaction.userID
        }

        return jsonify(transaction_data), 200
    except ValueError:
        return jsonify({'message': 'Invalid TransactionID format', 'code': 'INVALID_TRANSACTION_ID'}), 400
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/transaction_by_user_id', methods=['GET'])
def search_transaction_by_user_id():
    try:

        user_id = int(request.form.get('UserID'))

        transactions = Transaction.query.filter_by(userID=user_id).all()

        if not transactions:
            return jsonify({'message': 'No transactions found for the user', 'code': 'NO_TRANSACTIONS_FOUND'}), 404

        transaction_data = []
        for transaction in transactions:
            transaction_info = {
                'TransactionID': transaction.transactionID,
                'Username': transaction.username,
                'Amount': transaction.amount,
                'DateTime': transaction.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'TransactionType': transaction.transactionType,
                'Status': transaction.status,
                'UserID': transaction.userID
            }
            transaction_data.append(transaction_info)

        return jsonify(transaction_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/transaction_by_status', methods=['GET'])
def search_transaction_by_status():
    try:

        status = request.form.get('status')

        transactions = Transaction.query.filter_by(status=status).all()

        if not transactions:
            return jsonify(
                {'message': 'No transactions found with the given status', 'code': 'NO_TRANSACTIONS_FOUND'}), 404

        transaction_data = []
        for transaction in transactions:
            transaction_info = {
                'TransactionID': transaction.transactionID,
                'Username': transaction.username,
                'Amount': transaction.amount,
                'DateTime': transaction.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'TransactionType': transaction.transactionType,
                'Status': transaction.status,
                'UserID': transaction.userID
            }
            transaction_data.append(transaction_info)

        return jsonify(transaction_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/transaction_today', methods=['GET'])
def search_transaction_by_date_today():
    try:

        today_date = date.today()

        transactions = Transaction.query.filter(
            db.func.DATE(Transaction.dateTime) == today_date
        ).all()

        if not transactions:
            return jsonify({'message': 'No transactions found for today', 'code': 'NO_TRANSACTIONS_FOUND'}), 404

        transaction_data = []
        for transaction in transactions:
            transaction_info = {
                'TransactionID': transaction.transactionID,
                'Username': transaction.username,
                'Amount': transaction.amount,
                'DateTime': transaction.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'TransactionType': transaction.transactionType,
                'Status': transaction.status,
                'UserID': transaction.userID
            }
            transaction_data.append(transaction_info)

        return jsonify(transaction_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/transaction_week', methods=['GET'])
def search_transaction_by_date_week():
    try:

        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        transactions = Transaction.query.filter(
            db.func.DATE(Transaction.dateTime).between(start_of_week, end_of_week)
        ).all()

        if not transactions:
            return jsonify({'message': 'No transactions found for this week', 'code': 'NO_TRANSACTIONS_FOUND'}), 404

        transaction_data = []
        for transaction in transactions:
            transaction_info = {
                'TransactionID': transaction.transactionID,
                'Username': transaction.username,
                'Amount': transaction.amount,
                'DateTime': transaction.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'TransactionType': transaction.transactionType,
                'Status': transaction.status,
                'UserID': transaction.userID
            }
            transaction_data.append(transaction_info)

        return jsonify(transaction_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/transactions_month', methods=['GET'])
def search_transactions_by_month():
    try:

        current_month = datetime.now().month
        current_year = datetime.now().year

        transactions = Transaction.query.filter(
            db.extract('month', Transaction.dateTime) == current_month,
            db.extract('year', Transaction.dateTime) == current_year
        ).all()

        if not transactions:
            return jsonify(
                {'message': 'No transactions found for the current month', 'code': 'NO_TRANSACTIONS_FOUND'}), 404

        transaction_data = []
        for transaction in transactions:
            transaction_info = {
                'TransactionID': transaction.transactionID,
                'Username': transaction.username,
                'Amount': transaction.amount,
                'DateTime': transaction.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'TransactionType': transaction.transactionType,
                'Status': transaction.status,
                'UserID': transaction.userID
            }
            transaction_data.append(transaction_info)

        return jsonify(transaction_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/transactions_custom', methods=['GET'])
def search_transactions_by_custom_datetime():
    try:
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

        transactions = Transaction.query.filter(Transaction.dateTime.between(start_datetime, end_datetime)).all()

        if not transactions:
            return jsonify(
                {'message': 'No transactions found for the specified date range', 'code': 'NO_TRANSACTIONS_FOUND'}), 404

        transaction_data = []
        for transaction in transactions:
            transaction_info = {
                'TransactionID': transaction.transactionID,
                'Username': transaction.username,
                'Amount': transaction.amount,
                'DateTime': transaction.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'TransactionType': transaction.transactionType,
                'Status': transaction.status,
                'UserID': transaction.userID
            }
            transaction_data.append(transaction_info)

        return jsonify(transaction_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500



@app.route('/all_transactions', methods=['GET'])
def get_all_transactions():
    try:

        transactions = Transaction.query.all()

        transaction_data = []
        for transaction in transactions:
            transaction_info = {
                'TransactionID': transaction.transactionID,
                'Username': transaction.username,
                'Amount': transaction.amount,
                'DateTime': transaction.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'TransactionType': transaction.transactionType,
                'Status': transaction.status,
                'UserID': transaction.userID
            }
            transaction_data.append(transaction_info)

        return jsonify(transaction_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
