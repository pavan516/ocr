# Import from Rest Frameworks
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Import serializers
from .serializers import UsersSerializer
from .serializers import JwtTokensSerializer

# Import models
from .models import Users
from .models import JwtTokens

# Import Utilities
from app.utils.utils import Utils
from app.utils.mongo import Mongo

###
## Create your views here
###

#########################################################################################
#########################################################################################

### POST - USER LOGIN ENDPOINT ###
# Expected Payload
# {
#   "type": "GOOGLE",
#   "app_id": "123",
#   "name": "Pavan Kumar",
#   "email": "en.pavankumar@gmail.com",
#   "mobile": "8520872771",
#   "details": "I am software developer",
#   "image_url": "pavan.jpg"
# }
###
@api_view(['POST'])
def login(request):

  # payload
  payload = Utils.parseJson(request.body)

  # verify required fields exist
  verifyFields = Utils.verifyFields(payload, ['type','app_id','name','email','mobile','details','image_url'])
  if(len(verifyFields) > 0):
    return Response(Utils.errorResponse(verifyFields, "Bad Request"), 400)

  # mandatory fields check
  mandatoryFields = Utils.mandatoryFields(payload, ['type','app_id','name','email'])
  if(len(mandatoryFields) > 0):
    return Response(Utils.errorResponse(mandatoryFields, "Bad Request"), 400)

  # make sure type is APP
  if(payload['type'] != "GOOGLE"):
    return Response(Utils.errorResponse("Type must be GOOGLE, to login", "Bad Request"), 400)

  # fetch user with app_id
  user = []
  if(Users.objects.filter(app_id=payload['app_id'])).exists():
    userData = Users.objects.get(app_id=payload['app_id'])
    user = UsersSerializer(userData, many=False)
    user = user.data

  ###
  ## CASE1: if user does not exist create it
  ###
  if(len(user) == 0):

    # build users data to save record in DB
    userBody = {
      "uuid"        : Utils.uuid(),
      "app_id"      : payload['app_id'],
      "type"        : payload['type'],
      "name"        : payload['name'],
      "email"       : payload['email'],
      "mobile"      : payload['mobile'],
      "details"     : payload['details'],
      "image_url"   : payload['image_url'],
      "otp"         : "", # otp not required for GOOGLE LOGIN
      "verified"    : 1, # assume user is verified - FOR GOOGLE LOGIN
      "status"      : 1 # active
    }

    # save record in MYSQL DB
    serializer = UsersSerializer(data=userBody)
    if serializer.is_valid():
      serializer.save()
    else:
      return Response(Utils.errorResponse({'error':'Failed to create user'}), 500)

    # fetch user with app_id
    user = []
    if(Users.objects.filter(app_id=payload['app_id'])).exists():
      userData = Users.objects.get(app_id=payload['app_id'])
      user = UsersSerializer(userData, many=False)
      user = user.data

  ###
  ## CASE2: if user already exist update it
  ###
  if(len(user) > 0):

    # build users data to save record in DB
    user['name']      = payload['name']
    user['email']     = payload['email']
    user['image_url'] = payload['image_url']

    # save record in MYSQL DB
    serializer = UsersSerializer(userData, data=user)
    if serializer.is_valid():
      serializer.save()
    else:
      return Response(Utils.errorResponse({'error':'Failed to update user'}), 500)

  ###
  ## CASE3: create authentication token (JWT)
  ###

    # build jwt tokens data to save record in DB
    user['token'] = Utils.randomKeyGenerator(128)
    tokenBody = {
      "user_uuid"   : user['uuid'],
      "jwt_token"   : user['token']
    }

    # save record in MYSQL DB
    jwtSerializer = JwtTokensSerializer(data=tokenBody)
    if jwtSerializer.is_valid():
      jwtSerializer.save()
    else:
      return Response(Utils.errorResponse({'error':'Failed to generate JWT token'}), 500)

  # return response
  return Response(Utils.successResponse(user, "User loggedin successfully!"))

#########################################################################################
#########################################################################################

### GET - FETCH USERS ENDPOINT ###
# Expected Params
# 1. id
# 2. uuid
# 3. app_id
# 4. type
# 5. email
# 6. mobile
# 7. verified
# 8. status
###
@api_view(['GET'])
def fetchUsers(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # Build sql query
  sqlQuery = 'SELECT * FROM `users` WHERE '

  # filter with id
  if(request.GET['id']):
    sqlQuery += 'id = '+request.GET['id']+' AND '

  # filter with uuid
  if(request.GET['uuid']):
    sqlQuery += 'uuid = "'+request.GET['uuid']+'" AND '

  # filter with app_id
  if(request.GET['app_id']):
    sqlQuery += 'app_id = "'+request.GET['app_id']+'" AND '

  # filter with type
  if(request.GET['type']):
    sqlQuery += 'type = "'+request.GET['type']+'" AND '

  # filter with email
  if(request.GET['email']):
    sqlQuery += 'email = "'+request.GET['email']+'" AND '

  # filter with mobile
  if(request.GET['mobile']):
    sqlQuery += 'mobile = "'+request.GET['mobile']+'" AND '

  # filter with verified
  if(request.GET['verified']):
    sqlQuery += 'verified = '+request.GET['verified']+' AND '

  # filter with status
  if(request.GET['status']):
    sqlQuery += 'status = '+request.GET['status']+' AND '

  # sql query
  sqlQuery = sqlQuery.rstrip('WHERE ')
  sqlQuery = sqlQuery.rstrip('AND ')

  # execute raw sql query
  sql = Users.objects.raw(sqlQuery)
  data = UsersSerializer(sql, many=True).data

  # return response
  return Response(Utils.successResponse(data, "Users fetched successfully!"))

#########################################################################################
#########################################################################################

### PUT - UPDATE USER ENDPOINT ###
# Expected Payload
# {
#   "uuid": "user.uuid",
#   "name": "Pavan Kumar",
#   "email": "en.pavankumar@gmail.com",
#   "mobile": "8520872771",
#   "details": "I am software developer"
# }
###
@api_view(['PUT'])
def updateUser(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # payload
  payload = Utils.parseJson(request.body)

  # verify required fields exist
  verifyFields = Utils.verifyFields(payload, ['uuid','name','email','mobile','details'])
  if(len(verifyFields) > 0):
    return Response(Utils.errorResponse(verifyFields, "Bad Request"), 400)

  # mandatory fields check
  mandatoryFields = Utils.mandatoryFields(payload, ['uuid','name','email'])
  if(len(mandatoryFields) > 0):
    return Response(Utils.errorResponse(mandatoryFields, "Bad Request"), 400)

  # fetch user with uuid
  user = []
  if(Users.objects.filter(uuid=payload['uuid'])).exists():
    userData = Users.objects.get(uuid=payload['uuid'])
    user = UsersSerializer(userData, many=False)
    user = user.data

    # make sure sure exist
    if(len(user) == 0):
      return Response(Utils.errorResponse("User not found", "Bad Request"), 404)

    # build users data to save record in DB
    user['name']      = payload['name']
    user['email']     = payload['email']
    user['mobile']    = payload['mobile']
    user['details']   = payload['details']

    # save record in MYSQL DB
    serializer = UsersSerializer(userData, data=user)
    if serializer.is_valid():
      serializer.save()
    else:
      return Response(Utils.errorResponse({'error':'Failed to update user'}), 500)

  # return response
  return Response(Utils.successResponse(user, "User updated successfully!"))

#########################################################################################
#########################################################################################

### DELETE - DELETE LANGUAGE ENDPOINT ###
# Expected Param
# 1. uuid
###
@api_view(['DELETE'])
def deleteUser(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # filter with id
  uuid = 0
  if(request.GET['uuid']):
    uuid = request.GET['uuid']

  # make sure uuid is not empty
  if(uuid == 0):
    return Response(Utils.errorResponse("uuid is a mandatory param", "Bad Request"), 400)

  # TODO --- DELETE USER RELATED STUFF

  # delete record
  user = []
  if(Users.objects.filter(uuid=uuid)).exists():
    userData = Users.objects.get(uuid=uuid)
    userData.delete()
  else:
    return Response(Utils.errorResponse("User not found", "Bad Request"), 404)

  # return response
  return Response(Utils.successResponse("", "User deleted successfully!"), 204)

#########################################################################################
#########################################################################################

### GET - LOGOUT ENDPOINT ###
@api_view(['GET'])
def logout(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # delete token
  if(JwtTokens.objects.filter(jwt_token=authorize['token'])).exists():
    tokenData = JwtTokens.objects.get(jwt_token=authorize['token'])
    tokenData.delete()
  else:
    return Response(Utils.errorResponse("User not found", "Bad Request"), 404)

  # return response
  return Response(Utils.successResponse("", "User logged-out successfully!"), 204)

#########################################################################################
#########################################################################################
