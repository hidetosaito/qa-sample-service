#http://flask.pocoo.org/docs/0.10/tutorial/setup/


class Config(object):

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):

    # host
    HOST = '0.0.0.0'

    # dynamodb
    DYNAMODB_REGION = 'us-west-1'
    CRITERIA_TABLE = 'QAPortal-Staging-Criteria'
    RAW_TABLE = 'QAPortal-Staging-RawData'
    RESULT_TABLE = 'QAPortal-Staging-QAResult'

    # sqs
    SQS_REGIOM = 'us-west-1'
    SQS_NAME = 'QATaskQueue-Staging'
    
    # cache
    # http://pythonhosted.org/Flask-Cache/#configuring-flask-cache
    CACHE_TYPE = 'memcached'
    CACHE_MEMCACHED_SERVERS = ''
    CACHE_MEMCACHED_USERNAME = ''
    CACHE_MEMCACHED_PASSWORD = ''


class DevelopmentConfig(Config):

    # host
    HOST = '127.0.0.1'

    # dynamodb
    DYNAMODB_REGION = 'us-east-1'
    CRITERIA_TABLE = 'QAPortal-POC-Criteria'
    RAW_TABLE = 'QAPortal-POC-RawData'
    RESULT_TABLE = 'QAPortal-POC-QAResult'

    # sqs
    SQS_REGIOM = 'us-east-1'
    SQS_NAME = 'QATaskQueue-POC'
    
    # cache
    CACHE_TYPE = 'simple'


class DevelopmentContainerConfig(DevelopmentConfig):

    # host
    HOST = '0.0.0.0'


class TestConfig(Config):

    TESTING = True

    # host
    HOST = '0.0.0.0'

    # dynamodb
    DYNAMODB_REGION = 'us-east-1'
    CRITERIA_TABLE = 'test-Criteria'
    RAW_TABLE = 'test-RawData'
    RESULT_TABLE = 'test-QAResult'

    # sqs
    SQS_REGIOM = 'us-east-1'
    SQS_NAME = 'test-POC'
    
    # cache
    CACHE_TYPE = 'simple'
