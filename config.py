class DevelopmentConfig():
    DEBUG = True
    # Source DB conection
    DB_SOURCE_USERNAME = 'mneira'
    DB_SOURCE_PASSWORD = 'mneira'
    DB_SOURCE_DSN = 'localhost:1521/XEPDB1'
    DB_SOURCE_ENCODING = 'UTF-8'
    # Target DB #1 conection
    DB_T1_USERNAME = 'mneira'
    DB_T1_PASSWORD = 'mneira'
    DB_T1_DSN = 'localhost:1521/XEPDB1'
    DB_T1_ENCODING = 'UTF-8'
    # Target DB #2 conection
    DB_T2_USERNAME = 'report_app'
    DB_T2_PASSWORD = 'report'
    DB_T2_HOST = 'localhost'
    DB_T2_PORT = '3307'
    DB_T2_DB = 'reports'
    # Target DB #3 conection
    DB_T3_USERNAME = 'report_app'
    DB_T3_PASSWORD = 'report'
    DB_T3_HOST = 'localhost'
    DB_T3_PORT = '3307'
    DB_T3_DB = 'reports'

config = {
    'development' : DevelopmentConfig
}