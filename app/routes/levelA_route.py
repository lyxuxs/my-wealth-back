from datetime import datetime

from flask import request, jsonify

from app import app, db
from app.models.user_model import User
from app.models.levelA_model import  LevelA


@app.route('/getAllLevelA', methods=['GET'])
def getAllLevelA():
    try:
        levelAs = LevelA.query.all()
        levelAList = []
        for levelA in levelAs:
            levelA_data = {
                'refTreeID':levelA.refTreeID,
                'userID':levelA.userID,
                'friendUserID':levelA.friendUserID ,
                'isFriendAdmin':levelA.isFriendAdmin
            }
            levelAList.append(levelA_data)

        return jsonify(levelAList)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
    

@app.route('/userLevelA', methods=['GET'])
def userLevelA():
    try:
        user_id = request.args.get('userID')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
       
        levelAs = LevelA.query.filter_by(userID=user_id).all()
        levelAList = []
        for levelA in levelAs:
            levelA_data = {
                'refTreeID':levelA.refTreeID,
                'userID':levelA.userID,
                'friendUserID':levelA.friendUserID,
                'isFriendAdmin':levelA.isFriendAdmin
            }
            levelAList.append(levelA_data)

        return jsonify(levelAList)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500