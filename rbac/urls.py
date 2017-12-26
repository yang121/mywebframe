from django.conf.urls import url
from rbac import views

urlpatterns = [
    url(r'^sign-in.html', views.sign_in),
    url(r'^sign-up.html', views.sign_up),
    url(r'^sign-out', views.sign_out),
    url(r'^code', views.code),
    url(r'^upload/', views.upload),
]
