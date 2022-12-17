# Import from Django
from django.core import serializers

# Import from Rest Frameworks
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Import serializers
from .serializers import LanguagesSerializer

# Import models
from .models import Languages

# Import Utilities
from app.utils.utils import Utils
from app.utils.mongo import Mongo

###
## Create your views here
###

#########################################################################################
#########################################################################################

### GET - FETCH LANGUAGES ENDPOINT ###
# Expected Params
# 1. id
# 2. code
# 3. alpha2
# 4. alpha3
# 5. num
###
@api_view(['GET'])
def fetchLanguages(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # Build sql query
  sqlQuery = 'SELECT * FROM `languages` WHERE '

  # filter with id
  if(request.GET['id']):
    sqlQuery += 'id = '+request.GET['id']+' AND '

  # filter with code
  if(request.GET['code']):
    sqlQuery += 'code = "'+request.GET['code']+'" AND '

  # filter with alpha2
  if(request.GET['alpha2']):
    sqlQuery += 'alpha2 = "'+request.GET['alpha2']+'" AND '

  # filter with alpha3
  if(request.GET['alpha3']):
    sqlQuery += 'alpha3 = "'+request.GET['alpha3']+'" AND '

  # filter with num
  if(request.GET['num']):
    sqlQuery += 'num = "'+request.GET['num']+'" AND '

  # sql query
  sqlQuery = sqlQuery.rstrip('WHERE ')
  sqlQuery = sqlQuery.rstrip('AND ')

  # execute raw sql query
  sql = Languages.objects.raw(sqlQuery)
  data = LanguagesSerializer(sql, many=True).data

  # return response
  return Response(Utils.successResponse(data, "Languages fetched successfully!"))

#########################################################################################
#########################################################################################

### POST - CREATE LANGUAGE ENDPOINT ###
# Expected Payload
# {
#   "code": "",
#   "name": "",
#   "alpha2": "",
#   "alpha3": "",
#   "num": 0
# }
###
@api_view(['POST'])
def createLanguage(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # payload
  payload = Utils.parseJson(request.body)

  # verify required fields exist
  verifyFields = Utils.verifyFields(payload, ['code','name','alpha2','alpha3','num'])
  if(len(verifyFields) > 0):
    return Response(Utils.errorResponse(verifyFields, "Bad Request"), 400)

  # mandatory fields check
  mandatoryFields = Utils.mandatoryFields(payload, ['code','name','alpha3'])
  if(len(mandatoryFields) > 0):
    return Response(Utils.errorResponse(mandatoryFields, "Bad Request"), 400)

  # do not allow duplicte code
  if(Languages.objects.filter(code=payload['code'])).exists():
    return Response(Utils.errorResponse("Language already exist with this code", "Bad Request"), 400)

  # do not allow duplicte alpha3
  if(Languages.objects.filter(alpha3=payload['alpha3'])).exists():
    return Response(Utils.errorResponse("Language already exist with this alpha3", "Bad Request"), 400)

  # build users data to save record in DB
  languageBody = {
    "code"    : payload['code'],
    "name"    : payload['name'],
    "alpha2"  : payload['alpha2'],
    "alpha3"  : payload['alpha3'],
    "num"     : payload['num']
  }

  # save record in MYSQL DB
  serializer = LanguagesSerializer(data=languageBody)
  if serializer.is_valid():
    serializer.save()
  else:
    return Response(Utils.errorResponse({'error':'Failed to create language'}), 500)

  # return response
  return Response(Utils.successResponse(languageBody, "Language created successfully!"))

#########################################################################################
#########################################################################################

### PUT - UPDATE LANGUAGE ENDPOINT ###
# Expected Payload
# {
#   "id": "",
#   "code": "",
#   "name": "",
#   "alpha2": "",
#   "alpha3": "",
#   "num": 0
# }
###
@api_view(['PUT'])
def updateLanguage(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # payload
  payload = Utils.parseJson(request.body)

  # verify required fields exist
  verifyFields = Utils.verifyFields(payload, ['id','code','name','alpha2','alpha3','num'])
  if(len(verifyFields) > 0):
    return Response(Utils.errorResponse(verifyFields, "Bad Request"), 400)

  # mandatory fields check
  mandatoryFields = Utils.mandatoryFields(payload, ['id','code','name','alpha3'])
  if(len(mandatoryFields) > 0):
    return Response(Utils.errorResponse(mandatoryFields, "Bad Request"), 400)

  # do not allow duplicte code
  if(Languages.objects.filter(code=payload['code'])).exists():
    code = Languages.objects.get(code=payload['code'])
    codeData = LanguagesSerializer(code, many=False).data
    if(codeData['id'] != int(payload['id'])):
      return Response(Utils.errorResponse("Language already exist with this code", "Bad Request"), 400)

  # do not allow duplicte alpha3
  if(Languages.objects.filter(alpha3=payload['alpha3'])).exists():
    alpha3 = Languages.objects.get(alpha3=payload['alpha3'])
    alpha3Data = LanguagesSerializer(alpha3, many=False).data
    if(alpha3Data['id'] != int(payload['id'])):
      return Response(Utils.errorResponse("Language already exist with this alpha3", "Bad Request"), 400)

  # do not allow duplicte id
  language = []
  if(Languages.objects.filter(id=int(payload['id']))).exists():
    langData = Languages.objects.get(id=int(payload['id']))
    language = LanguagesSerializer(langData, many=False).data
    if(len(language) == 0):
      return Response(Utils.errorResponse("Language not found", "Bad Request"), 404)

    # build users data to save record in DB
    language['code'] = payload['code']
    language['name'] = payload['name']
    language['alpha2'] = payload['alpha2']
    language['alpha3'] = payload['alpha3']
    language['num'] = int(payload['num'])

    # save record in MYSQL DB
    serializer = LanguagesSerializer(langData, data=language)
    if serializer.is_valid():
      serializer.save()
    else:
      return Response(Utils.errorResponse({'error':'Failed to update language'}), 500)

  # return response
  return Response(Utils.successResponse(language, "Language updated successfully!"))

#########################################################################################
#########################################################################################

### DELETE - DELETE LANGUAGE ENDPOINT ###
# Expected Param
# 1. id
###
@api_view(['DELETE'])
def deleteLanguage(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # filter with id
  id = 0
  if(request.GET['id']):
    id = request.GET['id']

  # make sure id is not empty
  if(id == 0):
    return Response(Utils.errorResponse("id is a mandatory param", "Bad Request"), 400)

  # delete record
  language = []
  if(Languages.objects.filter(id=id)).exists():
    langData = Languages.objects.get(id=id)
    langData.delete()
  else:
    return Response(Utils.errorResponse("Language not found", "Bad Request"), 404)

  # return response
  return Response(Utils.successResponse("", "Language deleted successfully!"), 204)

# #########################################################################################
# #########################################################################################
