# IMPORT
from django.urls import path
from . import views

# URLS
urlpatterns = [
  path('v1/user/login', views.login),
  path('v1/users/fetch', views.fetchUsers),
  path('v1/user/update', views.updateUser),
  path('v1/user/delete', views.deleteUser),
  path('v1/user/logout', views.logout)
]
