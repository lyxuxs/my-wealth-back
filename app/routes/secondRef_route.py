from datetime import datetime

from flask import request, jsonify

from app import app, db
from app.models.user_model import User
from app.models.secondRef_model import  SecondRef


@app.route('/getAllSecondRef', methods=['GET'])
def getAllSecondRef():
    try:
        secondRefs = SecondRef.query.all()
        secondRefList = []
        for secondRef in secondRefs:
            secondRef_data = {
                'refTreeID':secondRef.refTreeID,
                'userID':secondRef.userID,
                'Ref':secondRef.Ref 
            }
            secondRefList.append(secondRef_data)

        response_data = {
            'secondRefs': secondRefList
        }
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
    

@app.route('/userSecondRef', methods=['GET'])
def userSecondRef():
    try:
        user_id = request.args.get('userID')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
       
        secondRefs = SecondRef.query.filter_by(userID=user_id).all()
        secondRefList = []
        for secondRef in secondRefs:
            secondRef_data = {
                'refTreeID':secondRef.refTreeID,
                'userID':secondRef.userID,
                'Ref':secondRef.Ref 
            }
            secondRefList.append(secondRef_data)

        response_data = {
            'secondRefs': secondRefList
        }
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500