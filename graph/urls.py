from django.urls import path
from . import views
from FansAlsoConnect.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path('', views.index, name='index'),
]