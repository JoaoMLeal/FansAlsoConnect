"""FansAlsoConnect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.apps import apps
from django.conf import settings

import bokeh
from bokeh.server.django import autoload, directory, document, static_extensions

from fansalsoconnect.apps.artistgraph.views import spotify_graph, spotify_graph_handler

bokeh_app_config = apps.get_app_config('bokeh.server.django')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('spotify_graph/', spotify_graph, name='spotify_graph'),
]

base_path = settings.BASE_PATH

bokeh_apps = [
    autoload('spotify_graph', spotify_graph_handler),
]

