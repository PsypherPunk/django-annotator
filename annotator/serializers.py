from rest_framework import serializers

from annotator.models import Range, Annotation


class RangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Range
        exclude = ("annotation", "id")


class AnnotationSerializer(serializers.ModelSerializer):
    """
    As per the documentation for ``django-rest-framework``:

        The default ModelSerializer ``.create()`` and ``.update()`` methods do
        not include support for writable nested representations.

    They therefore require explicit handling.
    """

    user = serializers.CharField(required=False)
    ranges = RangeSerializer(many=True)

    class Meta:
        model = Annotation
        fields = "__all__"

    def create(self, validated_data):
        """
        Create a new ``Annotation`` and related ``Range`` objects.

        :param validated_data: data for the new ``Annotation``.
        :return: newly-created ``Annotation``.
        """
        ranges_data = validated_data.pop("ranges")
        annotation = Annotation.objects.create(**validated_data)
        for range_data in ranges_data:
            Range.objects.create(annotation=annotation, **range_data)
        return annotation

    def update(self, instance, validated_data):
        """
        Here we ``delete()`` related ``Range`` objects and recreate.

        :param instance: ``Annotation`` to be updated.
        :param validated_data: data for the update.
        :return: updated ``Annotation``.
        """
        ranges_data = validated_data.pop("ranges")
        for field in validated_data.keys():
            setattr(instance, field, validated_data[field])
        instance.save()

        Range.objects.filter(annotation=instance).delete()
        for range_data in ranges_data:
            Range.objects.create(annotation=instance, **range_data)
        return instance
