from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('checks.urls'))
]