
class Config(object):
    pass

class Production(Config):
    SECRET_KEY = 'production_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/vlan.db'

class Development(Config):
    SECRET_KEY = 'development_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/vlan.db'

class DevelopmentMySQL(Config):
    SECRET_KEY = 'development_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://developer:developer@localhost/vlandb_development'