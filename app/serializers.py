# IMPORT SERIALIZERS
from rest_framework import serializers

# IMPORT MODELS
from app.models import SchemaVersion

# SchemaVersionSerializer
class SchemaVersionSerializer(serializers.ModelSerializer):
  class Meta:
    model     = SchemaVersion
    fields    = '__all__'