from rest_framework import serializers
from .models import Range, Annotation


class RangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Range
        fields = ("start", "end", "startOffset", "endOffset",)


class AnnotationSerializer(serializers.ModelSerializer):
    ranges = RangeSerializer(many=True)

    class Meta:
        model = Annotation
        fields = ("id", "annotator_schema_version", "created", "updated", "text", "quote", "uri", "user", "consumer", "ranges",)

    def create(self, validated_data):
        ranges_data = validated_data.pop("ranges")
        annotation = Annotation.objects.create(**validated_data)
        for range_data in ranges_data:
            Range.objects.create(annotation=annotation, **range_data)
        return annotation

    def update(self, instance, validated_data):
        ranges_data = validated_data.pop("ranges")
        for field in validated_data.keys():
            setattr(instance, field, validated_data[field])
        instance.save()
        # TODO: Support UPDATE for Ranges...
#        for range_data in ranges_data:
#            Range.objects.create(annotation=annotation, **range_data)
        return instance

