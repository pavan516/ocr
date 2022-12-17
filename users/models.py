### Import Models
from django.db import models

###
## Create your models here
###

# table name: users
class Users(models.Model):
  id          = models.AutoField(primary_key=True)
  uuid        = models.CharField(max_length=48)
  app_id      = models.CharField(max_length=255)
  type	      = models.CharField(max_length=64)
  name	      = models.CharField(max_length=255)
  email	      = models.CharField(max_length=255)
  mobile	    = models.CharField(max_length=18,blank=True,null=True)
  details	    = models.TextField(blank=True,null=True)
  image_url   = models.CharField(max_length=255)
  otp	        = models.CharField(max_length=12,blank=True,null=True)
  verified	  = models.IntegerField()
  status	    = models.IntegerField()
  class Meta:
    db_table  = "users"

# table name: jwt_tokens
class JwtTokens(models.Model):
  id          = models.AutoField(primary_key=True)
  user_uuid   = models.CharField(max_length=48)
  jwt_token   = models.CharField(max_length=255)
  class Meta:
    db_table  = "jwt_tokens"
