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


package_schema = PackageSchema()
main_admin_schema = MainAdminSchema()

admin_schema = AdminSchema()
