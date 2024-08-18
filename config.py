class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:HaPKSqNgYPAnjHQ3@localhost/my_wealth'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    MAIL_SERVER = 'mail.privateemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'noreply@mywealth.com.co'
    MAIL_PASSWORD = 'jyDbyt-2zavxy-zegrur'
    MAIL_DEFAULT_SENDER = 'noreply@mywealth.com.co'
