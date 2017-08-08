import django_filters

from annotator import models


class AnnotationFilterSet(django_filters.rest_framework.FilterSet):
    """
    Allow an ``icontains`` lookup on the ``text`` field.
    """
    text = django_filters.CharFilter(name="text",
                                     lookup_expr="icontains")

    class Meta:
        model = models.Annotation
        fields = (
            "text",
            "quote",
            "uri",
        )
