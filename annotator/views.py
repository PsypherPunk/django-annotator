from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import (HttpResponse,
                         HttpResponseForbidden,
                         HttpResponseBadRequest)
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import annotator
from annotator import models, serializers


class JSONResponse(HttpResponse):
    """
    An ``HttpResponse`` that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, **kwargs)


def root(request):
    if request.method == "GET":
        return JSONResponse({"name": getattr(settings,
                                             "ANNOTATOR_NAME",
                                             "django-annotator-store"),
                             "version": annotator.__version__})
    else:
        return HttpResponseForbidden()


@csrf_exempt
def index_create(request):
    if request.method == "GET":
        annotations = models.Annotation.objects.all()
        serializer = serializers.AnnotationSerializer(annotations, many=True)
        return JSONResponse(serializer.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = serializers.AnnotationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = HttpResponse(status=303)
            response["Location"] = reverse("read_update_delete",
                                           kwargs={"pk": serializer.data["id"]})
            return response
        else:
            return HttpResponseBadRequest(content=str(serializer.errors))
    else:
        return HttpResponseForbidden()


@csrf_exempt
def read_update_delete(request, pk):
    if request.method == "GET":
        annotation = get_object_or_404(models.Annotation, pk=pk)
        serializer = serializers.AnnotationSerializer(annotation)
        return JSONResponse(serializer.data, status=200)
    elif request.method == "PUT":
        annotation = get_object_or_404(models.Annotation, pk=pk)
        data = JSONParser().parse(request)
        serializer = serializers.AnnotationSerializer(annotation, data=data)
        if serializer.is_valid():
            serializer.save()
            response = HttpResponse(status=303)
            response["Location"] = reverse("read_update_delete",
                                           kwargs={"pk": serializer.data["id"]})
            return response
        else:
            return HttpResponseBadRequest(content=str(serializer.errors))
    elif request.method == "DELETE":
        annotation = get_object_or_404(models.Annotation, pk=pk)
        annotation.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponseForbidden()


def search(request):
    if request.method == "GET":
        query = {k: v for k, v in request.GET.items()}
        annotations = models.Annotation.objects.filter(**query)
        serializer = serializers.AnnotationSerializer(annotations, many=True)
        return JSONResponse({"total": len(serializer.data), "rows": serializer.data})
    else:
        return HttpResponseForbidden()


class DemoView(TemplateView):
    template_name = "annotator/demo.html"
