==================
django-annotations
==================

Django implementation of `annotatorjs Storage <http://annotatorjs.org/>`_.


Implements most of the methods as per the `Core Storage API <http://docs.annotatorjs.org/en/v1.2.x/storage.html#core-storage-api>`_ documentation (``root``, ``index``, ``create``, ``read``, ``update``, ``delete`` and ``search``).

To see a working demo:

.. code:: bash

    virtualenv annotatorjs
    cd annotatorjs
    source bin/activate
    git clone https://github.com/PsypherPunk/django-annotations.git
    cd django-annotations
    pip install -r requirements/base.txt
    ./manage.py runserver

A demo. page will then be available at ``/demo``.

