from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^userinfo', views.userinfo),
    url(r'^userinfo_json', views.userinfo_json),
    url(r'', views.backend),
]
