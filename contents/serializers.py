# IMPORT SERIALIZERS
from rest_framework import serializers

# IMPORT MODELS
from contents.models import Images

# ImagesSerializer
class ImagesSerializer(serializers.ModelSerializer):
  class Meta:
    model     = Images
    fields    = '__all__'
