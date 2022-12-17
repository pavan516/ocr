# IMPORT SERIALIZERS
from rest_framework import serializers

# IMPORT MODELS
from .models import Users
from .models import JwtTokens

# UsersSerializer
class UsersSerializer(serializers.ModelSerializer):
  class Meta:
    model     = Users
    fields    = '__all__'

# JwtTokensSerializer
class JwtTokensSerializer(serializers.ModelSerializer):
  class Meta:
    model     = JwtTokens
    fields    = '__all__'
