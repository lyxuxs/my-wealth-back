from datetime import date

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
