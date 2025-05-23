"""
Django settings for OrgSecure project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_6ph7e#l&q%1hg^m+lfmz68@2%efn9cb_z1^=4nomevt+mt3(f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'org_secure',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OrgSecure.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'OrgSecure.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'org_secure','static')

]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



ALLOWED_HOSTS = [ '127.0.0.2', 'mydomain.com']
# Custom configuration
KEY_FILE = os.getenv("KEY_FILE", "org_secure/assets/Key/public_key")
HASHING_DIRECTORY = os.getenv("HASHING_DIRECTORY", "org_secure/assets/hash")

HASHING_PARAM = {
    'n_dimensions': int(os.getenv("HASHING_N_DIMENSIONS", 128)),
    'n_tables': int(os.getenv("HASHING_N_TABLES", 15)),
    'n_projections': int(os.getenv("HASHING_N_PROJECTIONS", 40)),
}

CKKS_PARAM = {
    'poly_modulus_degree': int(os.getenv("CKKS_POLY_MODULUS_DEGREE", 8192)),
    'plain_modulus': int(os.getenv("CKKS_PLAIN_MODULUS", -1)),
    'coeff_mod_bit_sizes': eval(os.getenv("CKKS_COEFF_MOD_BIT_SIZES", "[60, 40, 40, 60]")),
}

BFV_PARAM = {
    'poly_modulus_degree': int(os.getenv("BFV_POLY_MODULUS_DEGREE", 8192)),
    'plain_modulus': int(os.getenv("BFV_PLAIN_MODULUS", 256)),
    'scale': int(os.getenv("BFV_SCALE", 10000)),
}

SERVER_URL = os.getenv("SERVER_URL", "http://127.0.0.1:8000/bio-encrypt-service")

URLS = {
    'registering_url': f'{SERVER_URL}/register/',
    'login': f'{SERVER_URL}/login/',
    'send_public_key': f'{SERVER_URL}/receive-public-key/',
    'send_hashing': f'{SERVER_URL}/receive-hashing/',
    'add_face': f'{SERVER_URL}/add-face/',
    'get_candidates': f'{SERVER_URL}/knerast/',
    'save_hashing': f'{SERVER_URL}/save-hashing/'
}


ENCRYPTION_CLASSES_DIRECTORY = 'org_secure.security'
ENCRYPTION_CLASSES = {
    "CKKS": f'{ENCRYPTION_CLASSES_DIRECTORY}.ckks_strategy.CKKSStrategy',
    "BFV": f'{ENCRYPTION_CLASSES_DIRECTORY}.bfv_strategy.BFVStrategy',
}

HASHING_CLASSES_DIRECTORY = 'org_secure.hashing'
HASHING_CLASSES = {
    "LSH": f'{HASHING_CLASSES_DIRECTORY}.lsh_strategy.LSHStrategy',
}

ENCRYPTION_STRATEGY = os.getenv("ENCRYPTION_STRATEGY", "CKKS")
HASHING_STRATEGY = os.getenv("HASHING_STRATEGY", "LSH")

MODEL_NAME = os.getenv("MODEL_NAME", "Facenet")

# Single user credentials
USER_CREDENTIALS = {
    "username": os.getenv("ORGNAME", "testuser"),
    "password": os.getenv("PASSWORD", "testpassword123"),
    "email":os.getenv("EMAIL", "test@example.com"),
    "encryption_type":os.getenv("ENCRYPTION_TYPE"),
}