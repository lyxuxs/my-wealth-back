from datetime import datetime

from flask import request, jsonify

from app import app, db
from app.models.profit_model import Profit
from app.models.trade_model import Trade


@app.route('/add_profit', methods=['POST'])
def add_profit():
    try:

        trade_id = int(request.form.get('TradeID'))
        profit_amount = float(request.form.get('ProfitAmount'))

        trade = Trade.query.get(trade_id)
        if not trade:
            return jsonify({'message': 'Trade not found', 'code': 'TRADE_NOT_FOUND'}), 404

        trade.trade_on_off = False
        db.session.commit()

        new_profit = Profit(
            tradeID=trade_id,
            profitAmount=profit_amount,
            dateTime=datetime.utcnow())

        db.session.add(new_profit)
        db.session.commit()

        response_data = {
            'ProfitID': new_profit.profitID,
            'TradeID': new_profit.tradeID,
            'ProfitAmount': new_profit.profitAmount,
            'DateTime': new_profit.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
            'message': 'Profit added successfully',
            'code': 200
        }

        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
