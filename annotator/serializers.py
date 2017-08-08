from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from annotator import models


class RangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Range
        exclude = ("annotation", "id")


class AnnotationSerializer(WritableNestedModelSerializer):
    user = serializers.CharField(required=False)
    ranges = RangeSerializer(many=True)

    class Meta:
        model = models.Annotation
        fields = "__all__"
