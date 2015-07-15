#http://flask.pocoo.org/docs/0.10/tutorial/setup/


class Config(object):

    DEBUG = True


class ProductionConfig(Config):

    # dynamodb
    DYNAMODB_REGION = 'us-west-1'
    CRITERIA_TABLE = 'QAPortal-Staging-Criteria'
    RAW_TABLE = 'QAPortal-Staging-RawData'
    RESULT_TABLE = 'QAPortal-Staging-QAResult'

    # sqs
    SQS_REGIOM = 'us-west-1'
    SQS_NAME = 'QATaskQueue-Staging'


class DevelopmentConfig(Config):

    # dynamodb
    DYNAMODB_REGION = 'us-east-1'
    CRITERIA_TABLE = 'QAPortal-POC-Criteria'
    RAW_TABLE = 'QAPortal-POC-RawData'
    RESULT_TABLE = 'QAPortal-POC-QAResult'

    # sqs
    SQS_REGIOM = 'us-east-1'
    SQS_NAME = 'QATaskQueue-POC'
