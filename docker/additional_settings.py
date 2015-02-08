import os
import random

if 'SECRET_KEY' not in os.environ:
    letters = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    r = random.SystemRandom()
    generated = ''.join([r.choice(letters) for i in range(50)])
    raise ValueError('''missing SECRET_KEY in environment.
You could use this random value :\n\n{}\n\n'''.format(generated))

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = 'DEBUG' in os.environ
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/db.sqlite3'
    }
}
MEDIA_ROOT = '/data/uploaded_files'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            },
        },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
