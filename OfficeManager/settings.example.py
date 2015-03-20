"""
Django settings for OfficeManager project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = '*'

TEMPLATE_DEBUG = True



# LDAP AD

import ldap
from django_auth_ldap.config import LDAPSearch

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)


AUTH_LDAP_SERVER_URI = "ldap://ad.example.com:389" 
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_START_TLS = False

# Allowing only users who are in group Employees
ORG_LDAP_BASE_DN = "CN=Users,DC=ad,DC=example,DC=com"

ORG_LDAP_GROUP="CN=Employees,%s" % ORG_LDAP_BASE_DN

ORG_LDAP_FILTER = "(&(objectClass=user)(memberof=%s))" % ORG_LDAP_GROUP

ORG_LDAP_SCOPE = "(&(objectClass=user)(memberof=%s)(sAMAccountName=%%(user)s))" % ORG_LDAP_GROUP


AUTH_LDAP_USER_SEARCH = LDAPSearch(ORG_LDAP_BASE_DN,
    ldap.SCOPE_SUBTREE, ORG_LDAP_SCOPE)




# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTH_LDAP_ALWAYS_UPDATE_USER = True



# email settings
EMAIL_HOST = "" 
EMAIL_PORT = None
EMAIL_HOST_USER = "" 
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True 
EMAIL_USE_SSL = False


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # not decided what to use, for later, jquery-ui for date pickers for sure
    'bootstrap3',
    'jquery_ui',
    
    'FrontPage',
    'TimeSheetManager',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'OfficeManager.urls'

WSGI_APPLICATION = 'OfficeManager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tbilisi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# this should go along with the prefix that isconfigured in the web server for the application
STATIC_URL = '/officemanager/static/'

# this is needed when deploying 
# to actually activate it one needs to run manage.py collectstatic to copy all files to where they should be server from
STATIC_ROOT = BASE_DIR + '/OfficeManager/static'


