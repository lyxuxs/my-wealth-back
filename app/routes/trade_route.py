from flask import jsonify, request

from app import app
from app import db
from app.models.trade_model import Trade


@app.route('/create_trade', methods=['POST'])
def create_trade():
    try:
        amount = float(request.form.get('Amount'))
        trade_on_off = bool(request.form.get('trade'))

        new_trade = Trade(amount=amount, trade_on_off=trade_on_off)
        db.session.add(new_trade)
        db.session.commit()

        response_data = {
            'tradeID': new_trade.tradeID,
            'amount': new_trade.amount,
            'datetime': new_trade.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'trade_on_off': new_trade.trade_on_off,
            'message': 'Trade created successfully',
            'code': 201
        }

        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/update_trade', methods=['PUT'])
def update_trade_on_off():
    try:
        trade_id = int(request.form.get('TradeID'))
        trade_on_off = bool(request.form.get('TradeOnOff'))

        trade = Trade.query.get(trade_id)
        if not trade:
            return jsonify({'message': 'Trade not found', 'code': 'TRADE_NOT_FOUND'}), 404

        trade.trade_on_off = trade_on_off
        db.session.commit()

        response_data = {
            'tradeID': trade.tradeID,
            'trade_on_off': trade.trade_on_off,
            'message': 'Trade on/off status updated successfully',
            'code': 200
        }

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
