from flask import jsonify, request
from app import app
from app import db
from app.models.commission_model import Commission


@app.route('/userTotalCommisson', methods=['GET'])
def get_user_total_commission():
    user_id = request.args.get('UserID')
    userCommissions = Commission.query.filter_by(userID=user_id).all()
    TotalCommission = sum(
        commission.commissionAmount for commission in userCommissions)

    response_data = {
        'TotalCommission': TotalCommission
    }

    return jsonify(response_data)


@app.route('/commission_by_user_id', methods=['GET'])
def search_commission_by_user_id():
    try:
        user_id = request.args.get('UserID')

        commissions = Commission.query.filter_by(userID=user_id).all()

        if not commissions:
            return jsonify({'message': 'No commissions found for the user', 'code': 'NO_COMMISSIONS_FOUND'}), 404

        commission_data = []
        for commission in commissions:
            commission_info = {
                'commissionID': commission.commissionID,
                'commissionAmount': commission.commissionAmount,
                'commissionType': commission.commissionType,
                'dateTime': commission.dateTime.strftime('%Y-%m-%d %H:%M:%S'),
                'userID': commission.userID,
            }
            commission_data.append(commission_info)

        return jsonify(commission_data), 200
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500


@app.route('/getAll_commisiions', methods=['GET'])
def getAll_commissions():
    commissions = Commission.query.all()

    response_data = []
    for commission in commissions:
        commission_data = {
            'commissionID': commission.commissionID,
            'commissionAmount': commission.commissionAmount,
            'commissionType': commission.commissionType,
            'dateTime': commission.dateTime,
            'userID': commission.userID,
        }
        response_data.append(commission_data)

    return jsonify(response_data)
