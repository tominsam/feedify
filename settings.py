# Django settings for feedify project.
import os

ROOT = os.path.dirname(__file__)

ADMINS = (
    ("Tom Insam", "tom@movieos.org"),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'default.db'),
    }
}

APPEND_SLASH = True

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

USE_ETAGS = True

MEDIA_ROOT = ''
MEDIA_URL = ''

SITE_URL="http://localhost:8002"

STATIC_URL='/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), "static"),
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
    #"debug_toolbar",

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
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'formatter': 'verbose',
        #     'filename': '/var/log/feedify/django.log',
        # },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO', # SQL loggiung on debug
            'handlers': ['console', "mail_admins"],
        },
        '': {
            'level': 'INFO', # SQL logging on debug
            'handlers': ['console', "mail_admins"],
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


FLICKR_REQUEST_TOKEN_URL="http://www.flickr.com/services/oauth/request_token"
FLICKR_ACCESS_TOKEN_URL="http://www.flickr.com/services/oauth/access_token"
FLICKR_AUTHORIZE_URL="http://www.flickr.com/services/oauth/authorize"

INSTAGRAM_AUTHORIZE_URL="https://api.instagram.com/oauth/authorize/"
INSTAGRAM_ACCESS_TOKEN_URL="https://api.instagram.com/oauth/access_token"
INSTAGRAM_API_URL="https://api.instagram.com/v1/"

FLICKR_API_URL="http://api.flickr.com/services/rest/"


PRODUCTION = os.environ.get("PRODUCTION", False)
if PRODUCTION:
    DEBUG=False
    EMAIL_BACKEND="sendmail.EmailBackend"
    SERVER_EMAIL="tom@movieos.org"
    DEFAULT_FROM_EMAIL="tom@movieos.org"
    STATIC_URL='http://feedify.movieos.org/static/'

    # ugh, hard-coding things sucks. Import production settings
    # from a python file in my home directory, rather than checking
    # them in.
    import imp
    prod = imp.load_source("production_settings", "/home/tomi/deploy/seatbelt/feedify_production.py")
    for k in filter(lambda a: a[0] != "_", dir(prod)):
        locals()[k] = getattr(prod, k)

else:
    DEBUG=True

    # these are dev keys
    FLICKR_API_KEY="2d56dbb2d5cf87796478b53e4949dc66"
    FLICKR_API_SECRET="c27d752ea2bdba80"

    # these are dev keys
    INSTAGRAM_API_KEY="2ee26d19721040c98b4f93da87d7b485"
    INSTAGRAM_API_SECRET="4acc3891a73147dfb77262b0daf3cc01"


TEMPLATE_DEBUG = DEBUG

