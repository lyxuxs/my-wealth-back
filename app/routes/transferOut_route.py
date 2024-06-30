from datetime import date
from datetime import datetime, timedelta

from flask import request, jsonify

from app import app, db
from app.models.transferOut_model import TransferOut
from app.models.user_model import User
from app.schemas import transferOut_schema


@app.route('/transferOut', methods=['POST'])
def create_transferout():
    data = request.form

    amount = float(data['amount'])
    user_id = int(data['userID'])

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404

    transferOut = TransferOut(
        dateTime=datetime.utcnow(),
        amount=amount,
        userID=user_id
    )
    db.session.add(transferOut)
    db.session.commit()

    transferOut_data = transferOut_schema.dump(transferOut)

    response_data = {
        'data&Time': transferOut_data['dateTime'],
        'Amount': amount,
        'TransferOutID': transferOut_data['transferID'],
        'UserID': user_id,
        'message': 'Create TransferOut',
        'code': 'TRANSFEROUT_CREATED'
    }

    return jsonify(response_data), 201


@app.route('/transferOut_search', methods=['GET'])
def search_transferOut_by_user_id():
    user_id = request.args.get('userID')

    if user_id is None:
        return jsonify({'message': 'User ID is required', 'code': 'USER_ID_REQUIRED'}), 400

    transferOuts = TransferOut.query.filter_by(userID=user_id).all()

    if not transferOuts:
        return jsonify({'message': 'No transfer outs found for the user', 'code': 'NO_TRANSFER_OUTS_FOUND'}), 404

    transferOuts_data = []
    for transferOut in transferOuts:
        transferOuts_data.append({
            'data&Time': transferOut.dateTime,
            'Amount': transferOut.amount,
            'TransferOutID': transferOut.transferID,
            'UserID': transferOut.userID
        })

    return jsonify(transferOuts_data), 200
