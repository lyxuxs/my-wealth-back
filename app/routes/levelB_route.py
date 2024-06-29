from datetime import datetime

from flask import request, jsonify

from app import app, db
from app.models.user_model import User
from app.models.levelB_model import  LevelB


@app.route('/getAllLevelB', methods=['GET'])
def getAllLevelB():
    try:
        levelBs = LevelB.query.all()
        levelBList = []
        for levelB in levelBs:
            levelB_data = {
                'refTreeID':levelB.refTreeID,
                'userID':levelB.userID,
                'friendUserID':levelB.friendUserID,
                'isFriendAdmin':levelB.isFriendAdmin 
            }
            levelBList.append(levelB_data)

        return jsonify(levelBList)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
    

@app.route('/userLevelB', methods=['GET'])
def userLevelB():
    try:
        user_id = request.args.get('userID')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
       
        levelBs = LevelB.query.filter_by(userID=user_id).all()
        levelBList = []
        for levelB in levelBs:
            levelB_data = {
                'refTreeID':levelB.refTreeID,
                'userID':levelB.userID,
                'friendUserID':levelB.friendUserID,
                'isFriendAdmin':levelB.isFriendAdmin 
            }
            levelBList.append(levelB_data)

        return jsonify(levelBList)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500