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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False  # 是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
EMAIL_USE_SSL = True  # 是否使用SSL加密，qq企业邮箱要求使用
EMAIL_HOST = 'smtp.qq.com'  # 发送邮件的邮箱 的 SMTP服务器，这里用了163邮箱
EMAIL_PORT = 465  # 发件箱的SMTP服务器端口
EMAIL_HOST_USER = '359580720@qq.com'  # 发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = 'oceaxurgyqbfbjge'  # 发送邮件的邮箱密码(这里使用的是授权码)