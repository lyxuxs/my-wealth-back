from datetime import datetime

from flask import request, jsonify

from app import app, db
from app.models.user_model import User
from app.models.thirdRef_model import  ThirdRef


@app.route('/getAllThirdRef', methods=['GET'])
def getAllThirdRef():
    try:
        thirdRefs = ThirdRef.query.all()
        thirdRefList = []
        for thirdRef in thirdRefs:
            thirdRef_data = {
                'refTreeID':thirdRef.refTreeID,
                'userID':thirdRef.userID,
                'Ref':thirdRef.Ref 
            }
            thirdRefList.append(thirdRef_data)

        response_data = {
            'thirdRefs': thirdRefList
        }
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
    

@app.route('/userThirdRef', methods=['GET'])
def userThirdRef():
    try:
        user_id = request.args.get('userID')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
       
        thirdRefs = ThirdRef.query.filter_by(userID=user_id).all()
        thirdRefList = []
        for thirdRef in thirdRefs:
            thirdRef_data = {
                'refTreeID':thirdRef.refTreeID,
                'userID':thirdRef.userID,
                'Ref':thirdRef.Ref 
            }
            thirdRefList.append(thirdRef_data)

        response_data = {
            'thirdRefs': thirdRefList
        }
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500