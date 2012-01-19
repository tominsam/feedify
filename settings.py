# Django settings for feedify project.
import os

ROOT = os.path.dirname(__file__)

PRODUCTION = os.environ.get("PRODUCTION", False) and True or False
try:
    from local_settings import *
except ImportError:
    pass

if PRODUCTION:
    DEBUG = False
else:
    DEBUG = True


TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ("Tom Insam", "tom@movieos.org")
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'feedify',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

APPEND_SLASH = True

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

MEDIA_ROOT = ''
MEDIA_URL = ''

if PRODUCTION:
    SITE_URL="http://feedify.movieos.org"
else:
    SITE_URL="http://localhost:8002"



ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_URL='/static'

if not PRODUCTION:
    STATICFILES_DIRS = (
        "static",
        ("admin", "venv/lib/python2.7/site-packages/django/contrib/admin/media"),
    )

SECRET_KEY = 'dev-secret-key'

SESSION_COOKIE_NAME = "feedify_session"

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "core.context_processors.all_settings",
)


MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'session.middleware.SessionMiddleware', # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.exception_handling.ExceptionMiddleware',
]

# if not PRODUCTION:
#     MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
#     INTERNAL_IPS = ('127.0.0.1',)
#     DEBUG_TOOLBAR_CONFIG = {
#         "INTERCEPT_REDIRECTS": False,
#     }


ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    # deps
    "south",
    "debug_toolbar",

    # my apps
    "core",
    "flickr",
    "instagram",
)

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s|%(asctime)s|%(process)d|%(module)s|%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': 'feedify_django.log',
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO', # SQL loggiung on debug
            'handlers': ['console', 'file'],
        },
        '': {
            'level': 'INFO', # SQL logging on debug
            'handlers': ['console', 'file'],
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
    

FLICKR_API_KEY="2d56dbb2d5cf87796478b53e4949dc66"
FLICKR_API_SECRET="c27d752ea2bdba80"
FLICKR_API_URL="http://api.flickr.com/services/rest/"

FLICKR_REQUEST_TOKEN_URL="http://www.flickr.com/services/oauth/request_token"
FLICKR_ACCESS_TOKEN_URL="http://www.flickr.com/services/oauth/access_token"
FLICKR_AUTHORIZE_URL="http://www.flickr.com/services/oauth/authorize"


if PRODUCTION:
    INSTAGRAM_API_KEY="de46f87ac84b42b4b9a6a0058adb855e"
    INSTAGRAM_API_SECRET="b83863d206dc4189976798ff5eae45e4"
else:
    INSTAGRAM_API_KEY="2ee26d19721040c98b4f93da87d7b485"
    INSTAGRAM_API_SECRET="4acc3891a73147dfb77262b0daf3cc01"

INSTAGRAM_AUTHORIZE_URL="https://api.instagram.com/oauth/authorize/"
INSTAGRAM_ACCESS_TOKEN_URL="https://api.instagram.com/oauth/access_token"
INSTAGRAM_API_URL="https://api.instagram.com/v1/"
