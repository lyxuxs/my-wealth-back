class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1a1a1a@localhost/my_wealth'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'investment.mywealth@gmail.com'
    MAIL_PASSWORD = 'kwns vldq aeza pafa'
    MAIL_DEFAULT_SENDER = 'investment.mywealth@gmail.com'

    SECRET_KEY = "secret_key"
    JWT_SECRET_KEY = "jwt_secret_key"
