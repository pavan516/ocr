# IMPORT
from django.urls import path
from . import views

# URLS
urlpatterns = [
  path('v1/languages/fetch', views.fetchLanguages),
  path('v1/language/create', views.createLanguage),
  path('v1/language/update', views.updateLanguage),
  path('v1/language/delete', views.deleteLanguage)
]
