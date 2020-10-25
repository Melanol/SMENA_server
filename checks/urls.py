from django.conf.urls import include, url
from . import views


urlpatterns = [
    # url(r'^django-rq/', include('django_rq.urls')),
    url(r'^create_checks/', views.create_checks),
    url(r'^new_checks/', views.new_checks),
    url(r'^check/', views.check),
]