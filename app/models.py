### Import Models
from django.db import models

###
## Create your models here
###

# table name: schema_version
class SchemaVersion(models.Model):
  id          = models.AutoField(primary_key=True)
  version     = models.CharField(max_length=18)
  modified_dt = models.DateTimeField()
  class Meta:
    db_table  = "schema_version"