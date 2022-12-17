# IMPORT SERIALIZERS
from rest_framework import serializers

# IMPORT MODELS
from .models import Languages

# LanguagesSerializer
class LanguagesSerializer(serializers.ModelSerializer):
  class Meta:
    model     = Languages
    fields    = '__all__'
