import os
from pathlib import Path


# settings.py

# settings.py

# settings.py

# settings.py

# settings.py

# settings.py

import environ

# Charger les variables d'environnement avec django-environ
env = environ.Env()
env.read_env()

# ...

# Utiliser les variables d'environnement
PAYPAL_RECEIVER_EMAIL = env('PAYPAL_RECEIVER_EMAIL', default='')
PAYPAL_CLIENT_ID = env('PAYPAL_CLIENT_ID', default='')
PAYPAL_SECRET_KEY = env('PAYPAL_SECRET_KEY', default='')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9d6%fod11=iaodpv)eby&#1z4(5@--&(t=m4s95w6jo7$!spju'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
#"ElhadjUFCC.pythonanywhere.com."

# settings.py

CORS_ALLOWED_ORIGINS = [
    "http://votre-frontend.com",
    # Ajoutez d'autres domaines autorisés au besoin
]


# Application definition



INSTALLED_APPS = [
    'paypal.standard.ipn',
    'paypal',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'fotoblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('templates'),  # <--- add this line
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'fotoblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'authentication.validators.ContainsLetterValidator',
    },
    {
        'NAME': 'authentication.validators.ContainsNumberValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.joinpath('static/')]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.User'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = LOGIN_URL

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media/')

#STATIC_ROOT = os.path.join(BASE_DIR, "static")
# settings.py
PAYPAL_RECEIVER_EMAIL='jallohelhadjabdul@gmail.com'
PAYPAL_CLIENT_ID='Af84vG-dNyVafwVXDCWXPrfGEWRcj6Wzp996ctIZD3gyD4Ohl-yEkh3d8lu4sbPDaoa_NhzQqxoRqWFg'
#PAYPAL_SECRET_KEY = 'votre_secret_key'
PAYPAL_MODE = 'sandbox'  # 'sandbox' ou 'live'
PAYPAL_TEST = True
#PAYPAL_BUY_BUTTON_IMAGE = 'https://res.cloudinary.com/the-proton-guy/image/upload/v1685882223/paypal-PhotoRoom_v9pay7.png'


#Envoi de mail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jallohelhadjabdul@gmail.com'
EMAIL_HOST_PASSWORD ='zjeqhfqrnoomevqh'