from flask_marshmallow import Marshmallow

ma = Marshmallow()


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('admin_id', 'user_name', 'email',
                  'password', 'otp', 'is_verified')


class MainAdminSchema(ma.Schema):
    class Meta:
        fields = ('email', 'name', 'password', 'adminReferral')


class PackageSchema(ma.Schema):
    class Meta:
        fields = ('packageID', 'packageName', 'personalMinFund',
                  'personalMaxFund', 'rebateFee')


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'userID',
            'name',
            'email',
            'password',
            'myReferral',
            'friendReferral',
            'spotBalance',
            'fundingBalance',
            'profit',
            'RT',
            'isVerify',
            'OTP',
            'packageID'
        )


class TransferSchema(ma.Schema):
    class Meta:
        fields = ('transferID', 'dateTime', 'amount', 'From', 'to', 'userID')


class TransferOutSchema(ma.Schema):
    class Meta:
        fields = ('transferOutID', 'dateTime', 'amount', 'userID')


class DepositSchema(ma.Schema):
    class Meta:
        fields = ('depositID', 'username', 'amount',
                  'dateTime', 'status', 'userID')


class TransactionSchema(ma.Schema):
    class Meta:
        fields = (
            'transactionID', 'username', 'amount', 'dateTime', 'transactionType', 'status', 'withdrawalID', 'depositID',
            'userID')


class WithdrawalSchema(ma.Schema):
    class Meta:
        fields = (
            'withdrawalID', 'username', 'amount', 'dateTime', 'withdrawalNetwork', 'withdrawalWalletAddress', 'status',
            'userID')


class TradeSchema(ma.Schema):
    class Meta:
        fields = ('tradeID', 'amount', 'dateTime', 'tradeOnOff')


class ProfitSchema(ma.Schema):
    class Meta:
        fields = ('profitID', 'profitAmount', 'dateTime', 'tradeID')


class UserProfitSchema(ma.Schema):
    class Meta:
        fields = ('userProfitID', 'profitType', 'profitAmount',
                  'dateTime', 'profitID', 'userID')


class LevelASchema(ma.Schema):
    class Meta:
        fields = ('refTreeID', 'userID', 'friendUserID', 'isFriendAdmin')


class LevelBSchema(ma.Schema):
    class Meta:
        fields = ('refTreeID', 'userID', 'friendUserID', 'isFriendAdmin')


class LevelCSchema(ma.Schema):
    class Meta:
        fields = ('refTreeID', 'userID', 'friendUserID', 'isFriendAdmin')


class CommissionSchema(ma.Schema):
    class Meta:
        fields = ('commissionID', 'commissionAmount',
                  'commissionType', 'dateTime', 'userID')


level_a_schema = LevelASchema()
level_b_schema = LevelBSchema()
level_c_schema = LevelCSchema()

user_schema = UserSchema()
package_schema = PackageSchema()
main_admin_schema = MainAdminSchema()
admin_schema = AdminSchema()
transfer_schema = TransferSchema()
transferOut_schema = TransferOutSchema()
deposit_schema = DepositSchema()
transaction_schema = TransactionSchema()
withdrawal_schema = WithdrawalSchema()
trade_schema = TradeSchema()
profit_schema = ProfitSchema()
user_profit_schema = UserProfitSchema()
commission_schema = CommissionSchema()
