"""
Django settings for ergo project.
"""
import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ADMINS = (('Kenny Ng', 'zqkng@stanford.edu'),)
MANAGERS = ADMINS

# SECURITY WARNNG: keep the secret key used in production secret!
DEFAULT_SECRET_KEY = '7!b7_=crh69qx@@8y@d(&amp;%nrxhkh6%-ud3q8km5=t3mqvdx-0j'
SECRET_KEY = os.environ.get('SECRET_KEY', DEFAULT_SECRET_KEY)

# SECRUITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'registration',
    'ergo',
    'ergo_info',
    'ergo_users',
    'ergo_contacts',
    'storages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ergo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ergo.wsgi.application'

SITE_ID=1

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATABASES = { 'default': dj_database_url.config() }

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')

# ALL all host headers
ALLOWED_HOSTS = ['*']

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
PROJECT_DIR = os.path.dirname(BASE_DIR)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(PROJECT_DIR, 'ergo_info/templates'),
    os.path.join(PROJECT_DIR, 'ergo_users/templates'),
    os.path.join(PROJECT_DIR, 'ergo_contacts/templates'),
)


# Absolute path to directory that will hold user-uploaded files.
# Used only in development (no S3).
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'

# Absolute path to directory that will hold static files.
# Used only in development (no S3).
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'

# Static asset configuration
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'staticfiles'),)

# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# session expiration
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window (can be any value)
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = 587
LOGIN_REDIRECT_URL = '/'

# Override local and sensitive settings information
try:
    from local_settings import *
except ImportError:
    pass

# Use S3 in production
if not DEBUG:
    AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME', '')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

    DEFAULT_FILE_STORAGE = 'ergo.s3util.MediaRootS3BotoStorage'
    STATICFILES_STORAGE = 'ergo.s3util.StaticRootS3BotoStorage'
    MEDIA_URL = 'https://{}.s3.amazonaws.com/media/'.format(AWS_S3_BUCKET_NAME)
    STATIC_URL = 'https://{}.s3.amazonaws.com/static/'.format(AWS_S3_BUCKET_NAME)
    ADMIN_MEDIA_PREFIX = 'https://{}.s3.amazonaws.com/static/admin/'.format(AWS_S3_BUCKET_NAME)
