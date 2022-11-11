from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.index, {'month': '2019/10/10'}),
    ]