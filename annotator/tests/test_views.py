import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from annotator import views


class IndexTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.index_create_url = reverse("index_create")
        self.read_update_delete_url = reverse("read_update_delete",
                                              kwargs={"pk": None})
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

    def create_annotation(self):
        request = self.factory.post(self.index_create_url,
                                    data=json.dumps(self.annotation),
                                    content_type="application/json")
        response = views.index_create(request)
        return response

    def test_index_create(self):
        request = self.factory.get(self.index_create_url)
        response = views.index_create(request)
        content = json.loads(response.content.decode("utf-8"))
        self.assertEquals(0, len(content))

        response = self.create_annotation()
        self.assertEquals(303, response.status_code)
        self.assertTrue(response.has_header("Location"))

        request = self.factory.get(self.index_create_url)
        response = views.index_create(request)
        content = json.loads(response.content.decode("utf-8"))
        self.assertEquals(1, len(content))

    def test_read_update_delete(self):
        self.create_annotation()
        request = self.factory.get(self.index_create_url)
        response = views.index_create(request)
        content = json.loads(response.content.decode("utf-8"))

        request = self.factory.get(self.read_update_delete_url)
        response = views.read_update_delete(request,
                                            content[0].get("id"))
        content = json.loads(response.content.decode("utf-8"))

        for key in self.annotation.keys():
            self.assertEquals(content.get(key), self.annotation.get(key))
