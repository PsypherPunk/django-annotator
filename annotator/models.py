import uuid
from django.db import models


class Annotation(models.Model):
    """
    Follows the `Annotation format <http://docs.annotatorjs.org/en/v1.2.x/annotation-format.html>`_,
    of ``annotatorjs``.

    :param annotator_schema_version: schema version: default v1.0
    :param created: created datetime
    :param updated: updated datetime
    :param text: content of annotation
    :param quote: the annotated text
    :param uri: URI of annotated document
    :param user: user id of annotation owner
    :param consumer: consumer key of backend
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    annotator_schema_version = models.CharField(max_length=8, default="v1.0")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
    quote = models.TextField()
    uri = models.CharField(max_length=4096, blank=True)
    user = models.CharField(max_length=128, blank=True)
    consumer = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ("created",)


class Range(models.Model):
    """
    Follows the `Annotation format <http://docs.annotatorjs.org/en/v1.2.x/annotation-format.html>`_,
    of ``annotatorjs``.

    :param start: (relative) XPath to start element
    :param end: (relative) XPath to end element
    :param startOffset: character offset within start element
    :param endOffset: character offset within end element
    :param annotation: related ``Annotation``
    """
    start = models.CharField(max_length=128)
    end = models.CharField(max_length=128)
    startOffset = models.IntegerField()
    endOffset = models.IntegerField()
    annotation = models.ForeignKey(Annotation, related_name="ranges")
