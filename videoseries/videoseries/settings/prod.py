from .base import *

DEBUG = False
ALLOWED_HOSTS = ['www.myhoast.com', ]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STRIPE_PUBLISHABLE_KEY = config('PUB_STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = config('PUB_STRIPE_SECRET_KEY')