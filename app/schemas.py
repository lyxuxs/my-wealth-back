from flask_marshmallow import Marshmallow

ma = Marshmallow()


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('admin_id', 'email', 'otp', 'token', 'is_verified')


admin_schema = AdminSchema()
