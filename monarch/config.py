DEBUG = False
ENABLE_DOC = "/"
SECRET_KEY = "U9b6o6c-uzEn3s1dSJxFm7tCY199cUTQ-7nFEbNGsyF4l6c1pX3oMbqImv20fRC_QOH3LigfeNGKyd0-Ua1jRQ=="

# SQLALCHEMY 配置
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/monarch?charset=utf8mb4"
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_MAX_OVERFLOW = 500
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 7200
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Redis 配置
REDIS_URL = "redis://127.0.0.1:6379/0"
REDIS_MAX_CONNECTIONS = 20

# Sentry DSN 配置
SENTRY_DSN = ""

# Celery 配置
CELERY_FORCE_ROOT = True
CELERY_TIMEZONE = "Asia/Shanghai"
BROKER_URL = "redis://127.0.0.1:6379/10"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/12"
CELERY_ACCEPT_CONTENT = ["pickle"]
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "pickle"
CELERY_ROUTES = {}
CELERYBEAT_SCHEDULE = {}

# SMS请求域名
SMS_BASE_URL = ""

# 统一登录中心
SSO_URL = "http://sso-dev.zhiyantek.com"

try:
    from local_settings import *  # noqa
except Exception as err:  # noqa
    pass
