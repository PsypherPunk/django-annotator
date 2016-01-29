from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from . import models
from . import serializers

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def root(request):
    return JSONResponse({"name": "The DataShed Annotation Store.", "version": "0.0.1"})


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
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
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
            print(serializer.validated_data)
            return HttpResponse(status=204)
    elif request.method == "DELETE":
        annotation = get_object_or_404(models.Annotation, pk=pk)
        annotation.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponseForbidden()


def search(request):
    if request.method == "GET":
        query = {k: v for k, v in request.GET.items()}
        print(models.Annotation.objects.filter(**query))
        return HttpResponse()
    else:
        return HttpResponseForbidden()
