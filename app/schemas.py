from flask_marshmallow import Marshmallow

ma = Marshmallow()


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('admin_id', 'user_name', 'email', 'password', 'otp', 'is_verified')


class MainAdminSchema(ma.Schema):
    class Meta:
        fields = ('email', 'name', 'password', 'adminReferral')


class PackageSchema(ma.Schema):
    class Meta:
        fields = ('packageID', 'packageName', 'personalMinFund', 'personalMaxFund', 'rebateFee')


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


class DepositSchema(ma.Schema):
    class Meta:
        fields = ('depositID', 'username', 'amount', 'dateTime', 'status', 'userID')


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


class MainRefSchema(ma.Schema):
    class Meta:
        fields = ('refTreeID', 'userID', 'Ref')


class SecondRefSchema(ma.Schema):
    class Meta:
        fields = ('refTreeID', 'userID', 'Ref')


class ThirdRefSchema(ma.Schema):
    class Meta:
        fields = ('refTreeID', 'userID', 'Ref')


main_ref_schema = MainRefSchema()
second_ref_schema = SecondRefSchema()
third_ref_schema = ThirdRefSchema()

user_schema = UserSchema()
package_schema = PackageSchema()
main_admin_schema = MainAdminSchema()
admin_schema = AdminSchema()
transfer_schema = TransferSchema()
deposit_schema = DepositSchema()
transaction_schema = TransactionSchema()
withdrawal_schema = WithdrawalSchema()
trade_schema = TradeSchema()
profit_schema = ProfitSchema()
