import os

from app.settings.base_settings import *


ALLOWED_HOSTS = [host for host in os.environ.get('ALLOWED_HOSTS').split(', ')]
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG=False
