"""
WSGI config for myweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'myweb.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myweb.settings")

if 'SERVER_SOFTWARE' in os.environ: #BAE
#	from django.core.handlers.wsgi import WSGIHandler 
	from django.core.wsgi import get_wsgi_application
	from bae.core.wsgi import WSGIApplication
#	application = WSGIApplication(WSGIHandler()) 
	application = WSGIApplication(get_wsgi_application())
else:
	from django.core.wsgi import get_wsgi_application
	application = get_wsgi_application()
