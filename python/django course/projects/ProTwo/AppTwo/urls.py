from django.urls import re_path
from django.urls import include
from AppTwo import views

urlpatterns = [
    re_path(r'^$', views.help, name='help')
]
