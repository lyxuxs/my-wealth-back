from datetime import datetime

from flask import request, jsonify

from app import app, db
from app.models.user_model import User
from app.models.levelC_model import  LevelC


@app.route('/getAllLevelC', methods=['GET'])
def getAllLevelC():
    try:
        levelCs = LevelC.query.all()
        levelCList = []
        for levelC in levelCs:
            levelC_data = {
                'refTreeID':levelC.refTreeID,
                'userID':levelC.userID,
                'friendUserID':levelC.friendUserID ,
                'isFriendAdmin':levelC.isFriendAdmin 
            }
            levelCList.append(levelC_data)

        return jsonify(levelCList) 
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500
    

@app.route('/userLevelC', methods=['GET'])
def userLevelC():
    try:
        user_id = request.args.get('userID')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
       
        levelCs = LevelC.query.filter_by(userID=user_id).all()
        levelCList = []
        for levelC in levelCs:
            levelC_data = {
                'refTreeID':levelC.refTreeID,
                'userID':levelC.userID,
                'friendUserID':levelC.friendUserID ,
                'isFriendAdmin':levelC.isFriendAdmin 
            }
            levelCList.append(levelC_data)

        return jsonify(levelCList)
    
    except Exception as e:
        return jsonify({'message': str(e), 'code': 'SERVER_ERROR'}), 500