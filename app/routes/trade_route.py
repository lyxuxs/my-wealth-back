from datetime import datetime

from flask import jsonify, request

from app import app
from app import db
from app.models.trade_model import Trade


@app.route('/create_trade', methods=['POST'])
def create_trade():
    try:
        amount = float(request.form.get('Amount'))
        trade_on_off = bool(request.form.get('trade'))

        current_datetime = datetime.now()

        new_trade = Trade(amount=amount, datetime=current_datetime, trade_on_off=trade_on_off)

        db.session.add(new_trade)
        db.session.commit()

        response_data = {
            'tradeID': new_trade.tradeID,
            'amount': new_trade.amount,
            'datetime': new_trade.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'trade_on_off': new_trade.trade_on_off,
            'message': 'Success',
            'code': 200
        }

        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
