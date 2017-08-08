import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from rest_framework.test import APIClient

import annotator
from annotator import models


class RootTestCase(TestCase):
    """
    See the documentation for the
    `root <http://docs.annotatorjs.org/en/v1.2.x/storage.html#root>`_
    endpoint.
    """

    def test_root(self):
        """
        Verifies that an object containing store metadata, including
        API version, is returned.
        """
        client = APIClient()
        response = client.get(reverse("root"))
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(200, response.status_code)
        self.assertListEqual(["name", "version"],
                             sorted(content.keys()))
        self.assertEqual(annotator.__version__,
                         content["version"])


class AnnotationTestCase(TestCase):
    """
    Base class with a few utility methods.

    The
    `documentation <http://docs.annotatorjs.org/en/v1.2.x/storage.html>`_
    at forms the basis for many of the tests.
    """

    def setUp(self):
        super(AnnotationTestCase, self).setUp()

        self.client = APIClient()
        self.index_create_url = reverse("annotations-list")
        self.annotation = {
            "annotator_schema_version": "v1.0",
            "text": "A note I wrote",
            "quote": "the text that was annotated",
            "uri": "http://example.com",
            "ranges": [
                {
                    "start": "/p[69]/span/span",
                    "end": "/p[70]/span/span",
                    "startOffset": 0,
                    "endOffset": 120
                }
            ]
        }

    def create_annotation(self, annotation=None):
        return self.client.post(self.index_create_url,
                                data=json.dumps(annotation or self.annotation),
                                content_type="application/json")


class IndexTestCase(AnnotationTestCase):
    """
    Tests methods on the index (i.e. ``/annotations``) route.
    """

    def test_create(self):
        """
        Verifies that, on receipt of an annotation object, a ``303``
        redirect is returned with an appropriate ``Location`` header.
        """
        response = self.client.get(self.index_create_url)
        content = json.loads(response.content.decode("utf-8"))
        self.assertEquals(0, len(content))

        response = self.create_annotation()

        self.assertEquals(303, response.status_code)
        self.assertTrue(response.has_header("Location"))

    def test_index(self):
        """
        Verifies that the index view returns a list of all annotation
        objects.
        """
        self.create_annotation()

        response = self.client.get(self.index_create_url)
        content = json.loads(response.content.decode("utf-8"))

        self.assertEquals(1, len(content))
        self.assertEqual(1, models.Annotation.objects.count())
        self.assertEqual(1, models.Range.objects.count())


class DetailTestCase(AnnotationTestCase):
    """
    Verifies the output of the detail view (i.e.
    ``/annotations/<id>``).
    """

    def test_read(self):
        """
        Verifies that an annotation object is returned.
        """
        response = self.create_annotation()

        response = self.client.get(response.get("Location"))
        content = json.loads(response.content.decode("utf-8"))

        for key in self.annotation.keys():
            self.assertEquals(content.get(key), self.annotation.get(key))

    def test_partial_update(self):
        """
        Verifies that on receipt of a partial annotation object, a
        ``303`` redirect is returned with an appropriate ``Location``
        header.
        """
        response = self.create_annotation()

        response = self.client.patch(response.get("Location"),
                                     data='{"text": "Another note I wrote."}',
                                     content_type="application/json")

        self.assertEquals(303, response.status_code)
        self.assertTrue(response.has_header("Location"))
        self.assertEqual(0, len(response.content))

        response = self.client.get(response.get("Location"))
        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content.get("text"), "Another note I wrote.")

    def test_delete(self):
        """
        Verifies that deletion of an annotation returns a ``204`` and
        no content.
        """
        response = self.create_annotation()
        self.assertEqual(1, models.Annotation.objects.count())
        self.assertEqual(1, models.Range.objects.count())

        response = self.client.delete(response.get("Location"))

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, len(response.content))
        self.assertEqual(0, models.Annotation.objects.count())
        self.assertEqual(0, models.Range.objects.count())


class SearchTestCase(AnnotationTestCase):
    """
    Verifies the output of the search (i.e. ``/search?text=spam``)
    endpoint.
    """

    def setUp(self):
        super(SearchTestCase, self).setUp()

        annotations = (
            ("man", "Well, what've you got?"),
            ("waitress", ("Well, there's egg and bacon; egg sausage and bacon; "
                          "egg and spam; egg bacon and spam; egg bacon sausage "
                          "and spam; spam bacon sausage and spam; spam egg "
                          "spam spam bacon and spam; spam sausage spam spam "
                          "bacon spam tomato and spam...")),
            ("vikings", "Spam spam spam spam..."),
            ("vikings", "Spam! Lovely spam! Lovely spam!")
        )
        annotation = self.annotation
        for k, v in annotations:
            annotation["text"] = v
            annotation["quote"] = k
            self.create_annotation(annotation)

    def test_search_exact(self):
        """
        Verifies that on receipt of a valid search, an object with
        ``total`` and ``rows`` fields is returned.
        """
        response = self.client.get(reverse("annotations-search"),
                                   data={"quote": "vikings"})
        content = json.loads(response.content.decode("utf-8"))

        self.assertListEqual(["rows", "total"],
                             sorted(content.keys()))
        self.assertEqual(2, content["total"])
        self.assertEqual(2, len(content["rows"]))

    def test_search_inexact(self):
        """
        All fields, save ``text`` should be exact matches.
        """
        response = self.client.get(reverse("annotations-search"),
                                   data={"quote": "viking"})
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(0, content["total"])
        self.assertEqual(0, len(content["rows"]))

    def test_search_text(self):
        """
        As per the examples for
        `search <http://docs.annotatorjs.org/en/v1.2.x/storage.html#search>`_,
        ``text`` should allow matches where the search term is
        *contained* in the ``text`` field.
        """
        response = self.client.get(reverse("annotations-search"),
                                   data={"text": "spam"})
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(3, content["total"])
        self.assertEqual(3, len(content["rows"]))