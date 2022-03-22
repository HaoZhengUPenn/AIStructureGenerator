from .base import *

DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gh_test',
        'OPTIONS': {
            # Tell MySQLdb to connect with 'utf8mb4' character set
            'charset': 'utf8mb4',
        },
        'USER':'tester',
        'PASSWORD':'363837',
        'HOST':'127.0.0.1',
        'PORT':3307,
        'CHARSET':'utf8'
    }
}