from datetime import datetime

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
