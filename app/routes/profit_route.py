from datetime import datetime

from flask import request, jsonify

from app import app, db
from app.models.profit_model import Profit
from app.models.trade_model import Trade
from app.models.user_model import User


@app.route('/add_profit', methods=['POST'])
def add_profit():
    try:
        trade_id = int(request.form.get('TradeID'))
        share_amount=request.form.get('shareAmount')
        profit_type=request.form.get('profitType')
        share_type=request.form.get('shareType')

        trade = Trade.query.get(trade_id)
        if not trade:
            return jsonify({'message': 'Trade not found', 'code': 'TRADE_NOT_FOUND'}), 404

        new_profit = Profit(
            tradeID=trade_id,
            shareAmount=share_amount,
            profitType=profit_type,
            shareType=share_type,
            dateTime=datetime.utcnow())

        db.session.add(new_profit)
        db.session.commit()
        
        trade.trade_on_off = False
        db.session.commit()
        
        rt_users = User.query.filter_by(RT=True).all()
        for user in rt_users:
            user.RT=False
            db.session.commit()

        response_data = {
            'ProfitID': new_profit.profitID,
            'TradeID': new_profit.tradeID,
            'share_amount':new_profit.shareAmount,
            'profit_type':new_profit.profitType,
            'share_type':new_profit.shareType,
            'DateTime': new_profit.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
            'message': 'Profit added successfully',
            'code': 200
        }

        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500

@app.route('/getAll_profit', methods=['GET'])
def getAll_profit():
    profits = Profit.query.all()

    response_data = []
    for profit in profits:
        profit_data = {
            'ProfitID': profit.profitID,
            'TradeID': profit.tradeID,
            'share_amount':profit.shareAmount,
            'profit_type':profit.profitType,
            'share_type':profit.shareType,
            'DateTime': profit.dateTime,
        }
        response_data.append(profit_data)

    return jsonify(response_data)
  