
from .base import *
DEBUG = False
ADMINS = (
    ('zixun HUANG', 'zixunhuang@outlook.com'),
)
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testdb',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
        'USER':'tester',
        'PASSWORD':'4X^t,`!n8Tdq',
        'HOST':'127.0.0.1',
        'PORT':3306,
        'CHARSET':'utf8'
    }
}
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
# REDIS_DB = 0