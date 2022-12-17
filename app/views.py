# Import from Django
from django.shortcuts import render
from django.core import serializers
from django.core.files.storage import default_storage

# Import from Rest Frameworks
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Import serializers
from .serializers import SchemaVersionSerializer

# Import models
from .models import SchemaVersion

# Import Utilities
from .utils.utils import Utils
from .utils.mongo import Mongo

# Import os, uuid
import os
import uuid
import json

###
## Create your views here
###

### GET - APP INFO ENDPOINT ###
@api_view(['GET'])
def info(request):

  # fetch version details from DB
  mysqlData = []
  if(SchemaVersion.objects.filter(id=1)).exists():
    mysqlVersion = SchemaVersion.objects.get(id=1)
    mysqlData = SchemaVersionSerializer(mysqlVersion, many=False)

  # create mongo connection & get collection
  collection = Mongo.mongo_conn('ocr_app')

  # find record with id = 1
  fetchMongoVersion = collection.find({"id":1})

  # parse mongo response
  mongoVersion = Mongo.parseMongoData(fetchMongoVersion, False)

  # get json path
  json_path = os.getcwd()+'/app/config/config.json'

  # read json file
  config = Utils.readJson(json_path)

  # Build app response
  data = {
    'app_name'          : config['name'],
    'app_code'          : config['code'],
    'app_version'       : config['version'],
    'db_mysql_version'  : mysqlData.data['version'],
    'db_mongo_version'  : mongoVersion['version'],
    'app_status'        : "",
    'app_author'        : config['author']
  }

  # if we fetch data from DB status is ok
  if(len(mysqlData.data) > 0):
    data['app_status'] = 'OK'

  # return response
  return Response(data)

#########################################################################################
#########################################################################################

### POST - SAVE FILE ENDPOINT ###
@api_view(['POST'])
def saveFile(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # Input file
  file=request.FILES['file']

  # build filename + save it
  uniqueId = str(uuid.uuid4())
  name = file.name.replace(" ", "_")
  filename = uniqueId+"_"+name
  file_name = default_storage.save("images/"+filename,file)

  # return response
  return Response({"file_name": file_name})
