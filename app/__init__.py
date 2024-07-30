from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.models import admin_model, levelA_model, levelB_model, levelC_model, mainAdmin_model, package_model, user_model, transfer_model,transferOut_model, withdrawal_model, \
    transaction_model, deposit_model, trade_model, profit_model, userProfit_model
from app.routes import admin_route, levelA_route, levelB_route, levelC_route, mainAdmin_route, package_route, user_route, transfer_route,transferOut_route, deposit_route, \
    withdrawal_route, transaction_route, profit_route, trade_route

with app.app_context():
    db.create_all()
