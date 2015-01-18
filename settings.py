# Django settings for ndov project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'nl'

SITE_ID = 4

LOGIN_URL = '/helpdesk/login/'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

LOCALE_PATHS= ('ndov/locale/', )

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/projects/ndov-helpdesk/static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    'ndov/static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5*#74p#taescig^(kresv4sv6up(ui8unnh1eez4&s*l2mo$@4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    'ndov/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
	'django.contrib.flatpages',
	'signup',
    'helpdesk',
	'south',
    #	'rosetta',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "logs/debug.log",
            'maxBytes': 5000000,
            'backupCount': 10,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'cli_actions':  {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}


QUEUE_EMAIL_BOX_TYPE = 'imap'
QUEUE_EMAIL_BOX_SSL = False

SIGNUP_UPLOAD_TO=MEDIA_ROOT
SIGNUP_ERROR_EMAIL=''

# These are overides over the default settings
HELPDESK_KB_ENABLED_STAFF = True
HELPDESK_TRANSLATE_TICKET_COMMENTS_LANG = ["en", "de", "fr", "it", "ru", "nl"]
HELPDESK_SHOW_CHANGE_PASSWORD = True
HELPDESK_SEND_SUBMITTER_EMAIL = False
HELPDESK_FILTER_LABEL_TO_QUEUE = True # This has priority over the next issue
HELPDESK_FILTER_CC_ALTERNATE = True # This will unfortunately move issues with a non existant label to this queue

HELPDESK_ALLOW_EDITOR_GROUP = True
HELPDESK_EDITOR_GROUP_NAME = 'Afnemers' 

try:
    from local_settings import *
except ImportError:
    pass
