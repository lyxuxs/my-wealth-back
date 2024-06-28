from datetime import datetime

from flask import request, jsonify

from app import app, db
from app.models.user_model import User
from app.models.mainRef_model import  MainRef


@app.route('/getAllMainRef', methods=['GET'])
def getAllMainRef():
    try:
        mainRefs = MainRef.query.all()
        mainRefList = []
        for mainRef in mainRefs:
            mainRef_data = {
                'refTreeID':mainRef.refTreeID,
                'userID':mainRef.userID,
                'Ref':mainRef.Ref 
            }
            mainRefList.append(mainRef_data)

        response_data = {
            'mainRefs': mainRefList
        }
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
    

@app.route('/userMainRef', methods=['GET'])
def userMainRef():
    try:
        user_id = request.args.get('userID')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
       
        mainRefs = MainRef.query.filter_by(userID=user_id).all()
        mainRefList = []
        for mainRef in mainRefs:
            mainRef_data = {
                'refTreeID':mainRef.refTreeID,
                'userID':mainRef.userID,
                'Ref':mainRef.Ref 
            }
            mainRefList.append(mainRef_data)

        response_data = {
            'mainRefs': mainRefList
        }
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500