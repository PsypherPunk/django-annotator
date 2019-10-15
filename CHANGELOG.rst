#########
Changelog
#########

All notable changes to this project will be documented in this file.

The format is based on
`Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`_
and this project adheres to
`Semantic Versioning <http://semver.org/spec/v2.0.0.html>`_.

[1.0.0] - 2017-02-21
====================

Migrated from the now-deprecated
`django-annotations <https://github.com/PsypherPunk/django-annotations>`_
project.

[1.0.1] - 2017-03-07
====================

Fixed
-----

- Correctly return a ``400`` if a request fails to validate; previously
no response was returned.

[2.0.0] - 2017-03-07
====================

Added
-----

- A ``FilterSet``, courtesy of ``django_filter``, to improve the
``/search`` functionality.

Changed
-------

- Replaced function-based-views with a
  ``rest_framework.viewsets.ModelViewSet``.
- Use ``drf-writable-nested`` to handle nested model interactions.
- Testing more focused around the Annotator
  `Storage <http://docs.annotatorjs.org/en/v1.2.x/storage.html>`_
  documentation.

[2.1.0] - 2019-10-15
====================

Added
-----

- This ``CHANGELOG``!
- Remove ``Django`` as an explict dependency in ``setup.py``.
- Include a ``MANIFEST.in`` to ensure the ``LICENCE`` and
  ``README.rst`` are included in the installation.

