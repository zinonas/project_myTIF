"""
Django settings for project_mytif project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


AUTH_USER_MODEL = 'auth.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i*l-m!4z86a#9!o-y5za5nv)!wt#jicdqc($g-b#vg7ha6^u!$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '213.7.247.244', 'www.enerca-tif.com']
#Template crispy_template_pack

CRISPY_TEMPLATE_PACK = 'bootstrap3'
#CRISPY_TEMPLATE_PACK = 'bootstrap'
#CRISPY_TEMPLATE_PACK = 'uni_form'
#CRISPY_TEMPLATE_PACK = 'foundation'


# Application definition

INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eReg',
    'crispy_forms',
    'bootstrap3',
    'pagination',
    'bootstrap3_datetime',
    'chartit',
    'simple_history',
    'simplejson',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)



ROOT_URLCONF = 'project_mytif.urls'

WSGI_APPLICATION = 'project_mytif.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cy_thal',
        'USER': 'root',
        'PASSWORD': '3wU4LaR^@!QAZ',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'enerca.tif@gmail.com'
EMAIL_HOST_PASSWORD = 'fnutxpbqxwjdzouu'#enerca2016

DEFAULT_FROM_EMAIL = 'enerca.tif@gmail.com'
SERVER_EMAIL = 'enerca.tif@gmail.com'


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

DATE_INPUT_FORMATS = ('%d-%m-%Y')

TIME_ZONE = 'Europe/Nicosia'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/enerca-tif/static'

#Template location
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "static", "templates"),
)

#NOT FOR THE LIVE VERSION
if DEBUG:
    MEDIA_URL = '/media/'
    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

    #FOR THE MEDIA UPLOADS
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "media")

    STATICFILES_DIRS = (
             os.path.join(os.path.dirname(BASE_DIR), "static", "static"),
       )



ADMIN_MEDIA_PREFIX = '/static/admin/img/'

BOOTSTRAP3 = {

    # The URL to the jQuery JavaScript file
    'jquery_url': '//code.jquery.com/jquery.min.js',

    # The Bootstrap base URL
    'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.2.0/',

    # The complete URL to the Bootstrap CSS file (None means derive it from base_url)
    'css_url': None,

    # The complete URL to the Bootstrap CSS file (None means no theme)
    'theme_url': None,

    # The complete URL to the Bootstrap JavaScript file (None means derive it from base_url)
    'javascript_url': None,

    # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap3.html)
    'javascript_in_head': False,

    # Include jQuery with Bootstrap JavaScript (affects django-bootstrap3 template tags)
    'include_jquery': True,

    # Label class to use in horizontal forms
    'horizontal_label_class': 'col-md-2',

    # Field class to use in horiozntal forms
    'horizontal_field_class': 'col-md-4',

    # Set HTML required attribute on required fields
    'set_required': True,

    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': True,

    # Class to indicate required (better to set this in your Django form)
    'required_css_class': '',

    # Class to indicate error (better to set this in your Django form)
    'error_css_class': 'has-error',

    # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
    'success_css_class': 'has-success',

    # Renderers (only set these if you have studied the source and understand the inner workings)
    'formset_renderers':{
        'default': 'bootstrap3.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
}
