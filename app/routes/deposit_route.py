from datetime import datetime

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
