#!/usr/bin/env python3

"""
Inspired by *The World's Smallest Django Project* in *Lightweight
Django*.


Intended as a minimal setup to run the ``demo`` application::

    ./demo.py

This will create a temporary SQLite database, perform ``test``,
``migrate`` and ``runserver`` commands, launching the ``demo``
application.
"""

import os
import random
import sys
import tempfile

import django
from django.conf import settings
from django.urls import include, path
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

DEBUG = os.environ.get("DEBUG", "on") == "on"

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "".join(
        [
            random.SystemRandom().choice(
                "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
            )
            for i in range(50)
        ]
    ),
)

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1").split(",")

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
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.staticfiles",
        "rest_framework",
        "django_filters",
        "annotator",
    ],
    STATIC_URL="/static/",
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.template.context_processors.tz",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ],
    REST_FRAMEWORK = {
        "DEFAULT_FILTER_BACKENDS": (
            "django_filters.rest_framework.DjangoFilterBackend",
        ),
    },
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": db.name,
        }
    },
)

django.setup()

urlpatterns = (path(r"", include("annotator.urls")),)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line([os.path.abspath(__file__), "test", "--verbosity=2"])
    execute_from_command_line([os.path.abspath(__file__), "migrate"])
    execute_from_command_line([os.path.abspath(__file__), "runserver"])
    os.unlink(db.name)
