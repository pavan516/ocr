### Import Models
from django.db import models

###
## Create your models here
###

# table name: images
class Images(models.Model):
  id          = models.AutoField(primary_key=True)
  uuid        = models.CharField(max_length=48)
  user_uuid   = models.CharField(max_length=48)
  title	      = models.CharField(max_length=255)
  description = models.TextField()
  image	      = models.CharField(max_length=255)
  language    = models.CharField(max_length=18)
  status	    = models.CharField(max_length=18)
  created_dt	= models.DateField()
  modified_dt = models.DateField()
  class Meta:
    db_table  = "images"
