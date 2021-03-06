import os

import eventlet
eventlet.monkey_patch()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
