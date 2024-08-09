from datetime import datetime
from flask import json, request, jsonify
from app import app, db
from app.models.userProfit_model import UserProfit
from app.models.user_model import User


@app.route('/getUserProfit', methods=['GET'])
def getUserProfit():
    userID = request.args.get('userID')
    userProfits = UserProfit.query.filter(UserProfit.userID == userID).all()

    response_data = []
    for userProfit in userProfits:
        UserProfit_data = {
            'userProfitID': userProfit.userProfitID,
            'DateTime': userProfit.dateTime,
            'TransactionType': userProfit.profitType,
            'Amount': userProfit.profitAmount,
            'profitID': userProfit.profitID,
            'userID': userProfit.userID,
        }
        response_data.append(UserProfit_data)

    return jsonify(response_data)


@app.route('/getAllUserProfit', methods=['GET'])
def getAllUserProfit():
    userProfits = UserProfit.query.all()

    response_data = []
    for userProfit in userProfits:
        UserProfit_data = {
            'userProfitID': userProfit.userProfitID,
            'DateTime': userProfit.dateTime,
            'TransactionType': userProfit.profitType,
            'Amount': userProfit.profitAmount,
            'profitID': userProfit.profitID,
            'userID': userProfit.userID,
        }
        response_data.append(UserProfit_data)

    return jsonify(response_data)
