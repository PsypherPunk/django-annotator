# `django-annotator`

Django implementation of [annotatorjs Storage](http://annotatorjs.org/).

Implements most of the methods as per the
[Core Storage/Search API](http://docs.annotatorjs.org/en/v1.2.x/storage.html#core-storage-api)
documentation (`root`, `index`, `create`, `read`, `update`,`delete` and
`search`).

To see a working demo:

``sh
poetry install
poetry run python3 ./demo.py
``

This will run the tests, after which a demo. page will be available at `/demo`.

## Installation

The package can be installed via `poetry`:

```sh
poetry add django-annotator
```

Following installation it can be added to any Django project by updating the
`INSTALLED_APPS`, along with its dependencies:

```python
INSTALLED_APPS = (
    ...
    "rest_framework",
    "django_filters",
    "annotator",
)
```

As per the integration
[documentation](https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html)
for `django-filter`, `DEFAULT_FILTER_BACKENDS` must also be added to
`settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
},
```

Then run `migrate` to include the new tables from `django-annotator`:

```sh
poetry run python3 ./manage.py migrate
```

## Annotator

The package relies on *Annotator* being installed in your project—see the
[documentation](http://docs.annotatorjs.org/en/v1.2.x/getting-started.html) for
details of its inclusion.

## Settings

As per Annotator's documentation, the
[root](http://docs.annotatorjs.org/en/v1.2.x/storage.html#root) endpoint will
return information in the format:

```json
{
    "name": "django-annotator-store",
    "version": "2.1.0"
}
```

The `name` returned can be configured by setting `ANNOTATOR_NAME` in your
`settings` (defaulting to the above).

## `django-cors-headers`

If you have any issues with *Cross-origin resource sharing (CORS)*, consider
installing
[`django-cors-headers`](https://github.com/ottoyiu/django-cors-headers).
