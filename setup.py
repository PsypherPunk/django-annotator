import os
from setuptools import find_packages, setup

import annotator

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-annotator",
    version=annotator.__version__,
    packages=find_packages(),
    include_package_data=True,
    description="Implementation of annotatorjs's Storage/Search API.",
    long_description=README,
    author="PsypherPunk",
    author_email="psypherpunk@gmail.com",
    url="https://github.com/PsypherPunk/django-annotator",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "Django",
        "djangorestframework",
    ],
)
