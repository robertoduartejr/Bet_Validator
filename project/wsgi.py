"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# from betvalidators import betvalidator
# import threading
# thread = threading.Thread(target=betvalidator)
# thread.start()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
