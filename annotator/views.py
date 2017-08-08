from django.conf import settings
from django.core import urlresolvers
from django.http.response import HttpResponseForbidden, JsonResponse
from django.views.generic import TemplateView

import django_filters
from rest_framework import status, viewsets
from rest_framework.response import Response

import annotator
from annotator import filters, models, serializers


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = models.Annotation.objects.all()
    serializer_class = serializers.AnnotationSerializer
    filter_class = filters.AnnotationFilterSet
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def root(self, _):
        """
        Implements the
        `root <http://docs.annotatorjs.org/en/v1.2.x/storage.html#root>`_
        endpoint.

        :param _:
            :class:`rest_framework.request.Request` object—ignored here.
        :return:
            API information :class:`rest_framework.response.Response`.
        """
        return JsonResponse(
            {
                "name": getattr(settings,
                                "ANNOTATOR_NAME",
                                "django-annotator-store"),
                "version": annotator.__version__
            })

    def search(self, _):
        """
        Implements the
        `search <http://docs.annotatorjs.org/en/v1.2.x/storage.html#search>`_
        endpoint.

        We rely on the behaviour of the ``filter_backends`` to manage
        the actual filtering of search results.

        :param _:
            :class:`rest_framework.request.Request` object—ignored here
            as we rely on the ``filter_backends``.
        :return:
            filtered :class:`rest_framework.response.Response`.
        """
        queryset = super(AnnotationViewSet, self).filter_queryset(
            self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "total": len(serializer.data),
            "rows": serializer.data
        })

    def get_success_headers(self, data):
        """
        As per the *Annotator* documentation regarding the
        `create <http://docs.annotatorjs.org/en/v1.2.x/storage.html#create>`_
        and
        `update <http://docs.annotatorjs.org/en/v1.2.x/storage.html#update>`_
        endpoints, we must return an absolute URL in the ``Location``
        header.
        :param data:
            serialized object.
        :return:
            :class:`dict` of HTTP headers.
        """
        headers = super(AnnotationViewSet, self).get_success_headers(data)

        url = urlresolvers.reverse("annotations-detail",
                                   kwargs={"pk": data["id"]})
        headers.update({"Location": self.request.build_absolute_uri(url)})

        return headers

    def create(self, request, *args, **kwargs):
        """
        See the *Annotator* documentation regarding the
        `create <http://docs.annotatorjs.org/en/v1.2.x/storage.html#create>`_
        endpoint.

        :param request:
            incoming :class:`rest_framework.request.Request`.
        :return:
            303 :class:`rest_framework.response.Response`.
        """
        response = super(AnnotationViewSet, self).create(request,
                                                         *args,
                                                         **kwargs)
        response.data = None
        response.status_code = status.HTTP_303_SEE_OTHER
        return response

    def update(self, request, *args, **kwargs):
        """
        See the *Annotator* documentation regarding the
        `update <http://docs.annotatorjs.org/en/v1.2.x/storage.html#update>`_
        endpoint.

        :param request:
            incoming :class:`rest_framework.request.Request`.
        :return:
            303 :class:`rest_framework.response.Response`.
        """
        response = super(AnnotationViewSet, self).update(request,
                                                         *args,
                                                         **kwargs)
        for h, v in self.get_success_headers(response.data).items():
            response[h] = v
        response.data = None
        response.status_code = status.HTTP_303_SEE_OTHER
        return response


class DemoView(TemplateView):
    template_name = "annotator/demo.html"
