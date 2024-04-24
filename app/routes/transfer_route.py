from datetime import date
from datetime import datetime, timedelta

from flask import request, jsonify

from app import app, db
from app.models.transfer_model import Transfer
from app.models.user_model import User
from app.schemas import transfer_schema


@app.route('/transfer', methods=['POST'])
def create_transfer():
    data = request.form

    amount = float(data['amount'])
    from_account = data['From']
    to_account = data['to']
    user_id = int(data['userID'])

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404

    valid_account_types = ['spotBalance', 'fundingBalance']
    if from_account not in valid_account_types or to_account not in valid_account_types:
        return jsonify({'message': 'Invalid account type', 'code': 'INVALID_ACCOUNT_TYPE'}), 400

    if from_account == 'spotBalance':
        balance_type = 'spotBalance'
    else:
        balance_type = 'fundingBalance'

    if getattr(user, balance_type) < amount:
        return jsonify({'message': 'Insufficient balance', 'code': 'INSUFFICIENT_BALANCE'}), 400

    setattr(user, balance_type, getattr(user, balance_type) - amount)
    setattr(user, to_account, getattr(user, to_account) + amount)

    transfer = Transfer(
        dateTime=datetime.utcnow(),
        amount=amount,
        From=from_account,
        to=to_account,
        userID=user_id
    )
    db.session.add(transfer)
    db.session.commit()

    transfer_data = transfer_schema.dump(transfer)

    response_data = {
        'data&Time': transfer_data['dateTime'],
        'Amount': amount,
        'From': from_account,
        'to': to_account,
        'TransferID': transfer_data['transferID'],
        'UserID': user_id,
        'message': 'Create Transfer',
        'code': 'TRANSFER_CREATED'
    }

    return jsonify(response_data), 201


@app.route('/transfer_search', methods=['GET'])
def search_transfer_by_user_id():
    user_id = request.form.get('userID')

    if user_id is None:
        return jsonify({'message': 'User ID is required', 'code': 'USER_ID_REQUIRED'}), 400

    transfers = Transfer.query.filter_by(userID=user_id).all()

    if not transfers:
        return jsonify({'message': 'No transfers found for the user', 'code': 'NO_TRANSFERS_FOUND'}), 404

    transfer_data = []
    for transfer in transfers:
        transfer_data.append({
            'data&Time': transfer.dateTime,
            'Amount': transfer.amount,
            'From': transfer.From,
            'to': transfer.to,
            'TransferID': transfer.transferID,
            'UserID': transfer.userID
        })

    return jsonify(transfer_data), 200


@app.route('/search_today', methods=['GET'])
def search_transfer_by_user_and_date_today():
    try:

        user_id = int(request.form.get('userID'))

        today = date.today()

        transfers = Transfer.query.filter_by(userID=user_id).filter(
            db.func.date(Transfer.dateTime) == today
        ).all()

        if not transfers:
            return jsonify({'message': 'No transfers found for the user and today', 'code': 'NO_TRANSFERS_FOUND'}), 404

        response_data = []
        for transfer in transfers:
            transfer_info = {
                'data&Time': transfer.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Amount': transfer.amount,
                'From': transfer.From,
                'to': transfer.to,
                'TransferID': transfer.transferID,
                'UserID': transfer.userID,
                'message': 'Transfer details for the user and today',
                'Code': 'TRANSFER_DETAILS'
            }
            response_data.append(transfer_info)

        return jsonify(response_data), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {'message': 'An error occurred while processing the request', 'error': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/search_week', methods=['GET'])
def search_transfer_by_user_and_date_this_week():
    try:

        user_id = int(request.form.get('userID'))

        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        transfers = Transfer.query.filter_by(userID=user_id).filter(
            Transfer.dateTime >= start_of_week,
            Transfer.dateTime <= end_of_week
        ).all()

        if not transfers:
            return jsonify({'message': 'No transfers found for the user this week', 'code': 'NO_TRANSFERS_FOUND'}), 404

        response_data = []
        for transfer in transfers:
            transfer_info = {
                'data&Time': transfer.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Amount': transfer.amount,
                'From': transfer.From,
                'to': transfer.to,
                'TransferID': transfer.transferID,
                'UserID': transfer.userID,
                'message': 'Transfer details for the user this week',
                'Code': 'TRANSFER_DETAILS'
            }
            response_data.append(transfer_info)

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/search_month', methods=['GET'])
def search_transfer_by_user_and_date_this_month():
    try:

        user_id = int(request.form.get('userID'))

        today = datetime.today()
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - timedelta(days=1)

        transfers = Transfer.query.filter_by(userID=user_id).filter(
            Transfer.dateTime >= start_of_month,
            Transfer.dateTime <= end_of_month
        ).all()

        if not transfers:
            return jsonify({'message': 'No transfers found for the user this month', 'code': 'NO_TRANSFERS_FOUND'}), 404

        response_data = []
        for transfer in transfers:
            transfer_info = {
                'data&Time': transfer.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'Amount': transfer.amount,
                'From': transfer.From,
                'to': transfer.to,
                'TransferID': transfer.transferID,
                'UserID': transfer.userID,
                'message': 'Transfer details for the user this month',
                'Code': 'TRANSFER_DETAILS'
            }
            response_data.append(transfer_info)

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
