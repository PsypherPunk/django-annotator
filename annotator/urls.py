from django.conf.urls import url

from rest_framework.routers import format_suffix_patterns

from annotator import views

annotations_list = views.AnnotationViewSet.as_view({
    "get": "list",
    "post": "create",
})

annotations_detail = views.AnnotationViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

annotations_search = views.AnnotationViewSet.as_view({
    "get": "search",
})

annotations_root = views.AnnotationViewSet.as_view({
    "get": "root",
})

urlpatterns = format_suffix_patterns([
    url(r"^demo/?$", views.DemoView.as_view(), name="demo"),
    url(r"^$", annotations_root, name="root"),
    url(r"annotations/?$", annotations_list, name="annotations-list"),
    url(r"annotations/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/?$",
        annotations_detail,
        name="annotations-detail"),
    url(r"search/?$", annotations_search, name="annotations-search"),
])
