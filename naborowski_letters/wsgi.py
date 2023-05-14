"""
WSGI config for naborowski_letters project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

import nltk
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naborowski_letters.settings.railway')


nltk.download('punkt')

application = get_wsgi_application()
