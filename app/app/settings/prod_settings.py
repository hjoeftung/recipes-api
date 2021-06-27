import os

from app.settings.base_settings import *


SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = [host for host in os.getenv('ALLOWED_HOSTS').split(', ')]
DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
