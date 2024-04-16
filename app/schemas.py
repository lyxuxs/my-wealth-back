from flask_marshmallow import Marshmallow

ma = Marshmallow()


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('admin_id', 'user_name', 'email', 'password', 'otp', 'is_verified')


admin_schema = AdminSchema()
