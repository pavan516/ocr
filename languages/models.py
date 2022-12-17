### Import Models
from django.db import models

###
## Create your models here
###

# table name: languages
class Languages(models.Model):
  id      = models.AutoField(primary_key=True)
  code    = models.CharField(max_length=64)
  name    = models.CharField(max_length=64)
  alpha2  = models.CharField(max_length=8)
  alpha3  = models.CharField(max_length=8)
  num     = models.IntegerField(max_length=8)
  class Meta:
    db_table  = "languages"
