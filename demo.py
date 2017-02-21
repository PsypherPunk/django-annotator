#!/usr/bin/env python

"""
Inspired by *The World's Smallest Django Project* in *Lightweight Django*.


Intended as a minimal setup to run the ``demo`` application::

    ./demo.py

This will create a temporary SQLite database, perform ``migrate`` and
``runserver`` commands, launching the ``demo`` application.
"""

import os
import random
import sys
import tempfile

from django.conf import settings
from django.conf.urls import include, url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

DEBUG = os.environ.get("DEBUG", "on") == "on"

SECRET_KEY = os.environ.get("SECRET_KEY",
                            "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789\!@#$%^&*(-_=+)") for i in range(50)]))

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS",
                               "127.0.0.1").split(",")

db = tempfile.NamedTemporaryFile(delete=False)
settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ),
    INSTALLED_APPS=["django.contrib.auth",
                    "django.contrib.contenttypes",
                    "django.contrib.staticfiles",
                    "annotator"],
    STATIC_URL="/static/",
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": db.name,
        }
    }
)


urlpatterns = (
    url(r"^/?", include("annotator.urls")),
)


application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line([os.path.abspath(__file__), "test"])
    execute_from_command_line([os.path.abspath(__file__), "migrate"])
    execute_from_command_line([os.path.abspath(__file__), "runserver"])
    db.delete()
    os.unlink(db.name)

