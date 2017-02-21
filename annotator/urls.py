from django.conf.urls import include, url

from annotator import views

urlpatterns = [
    url(r"^$", views.root, name="root"),
    url(r"^annotations/?$", views.index_create, name="index_create"),
    url(r"^annotations/(?P<pk>.+)/?$", views.read_update_delete, name="read_update_delete"),
    url(r"^search/?$", views.search, name="search"),
    url(r"^demo/?$", views.DemoView.as_view(), name="demo"),
]
