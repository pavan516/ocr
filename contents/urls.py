# IMPORT
from django.urls import path
from . import views

# URLS
urlpatterns = [
  path('v1/contents/fetch', views.fetch),
  path('v1/contents/create', views.create),
  path('v1/contents/segmentation/comment/create', views.createSegmentationComment),
  path('v1/contents/segmentation/comment/update', views.updateSegmentationComment),
  # path('v1/contents/segmentation/comment/delete', views.deleteSegmentationComment)
]
