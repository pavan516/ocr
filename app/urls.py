# IMPORT
from django.urls import path
from . import views

# URLS
urlpatterns = [
  path('info', views.info),
  path('file/save', views.saveFile),
]
