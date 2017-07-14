#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/alquranlearningcenter/app/")

from web import app as application
application.secret_key = 'Al-Quran Learning Center'
