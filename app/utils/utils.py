# Import required
import json
import uuid
import string
import random
import requests

# Import serializers
from users.serializers import UsersSerializer
from users.serializers import JwtTokensSerializer

# Import models
from users.models import Users
from users.models import JwtTokens

# Utils class
class Utils:

#########################################################################################
#########################################################################################

  # Method: errorResponse
  # Description: Build error response data
  # params: void (data), string message, string status, int code
  # response: json object
  def errorResponse(data, message='Something went wrong', status='error', code=0):

    # Build result
    result = {
      "status": status,
      "code": code,
      "message": message,
      "data": data
    }

    # return
    return result

#########################################################################################
#########################################################################################

  # Method: successResponse
  # Description: Build success response data
  # params: void (data), string message, string status, int code
  # response: json object
  def successResponse(data, message='Successfully fetched data', status='success', code=1):

    # Build result
    result = {
      "status": status,
      "code": code,
      "message": message,
      "data": data
    }

    # return
    return result

#########################################################################################
#########################################################################################

  # Method: verifyFields
  # Description: verify keys exist in json object
  # params: string (jsonData), array keys
  # response: array
  def verifyFields(jsonData, keys):

    # Init var
    data = []

    # loop keys
    for key in keys:
      # verify key exist
      if key not in jsonData:
        data.append("missing key {"+key+"} from payload!")

    # return data
    return data

#########################################################################################
#########################################################################################

  # Method: mandatoryFields
  # Description: make sure specified fields are not empty
  # params: string (jsonData), array keys
  # response: array
  def mandatoryFields(jsonData, keys):

    # Init var
    data = []

    # loop keys
    for key in keys:
      # verify key exist
      if(len(jsonData[key]) == 0):
        data.append("{"+key+"} is a mandatory field!")

    # return data
    return data

#########################################################################################
#########################################################################################

  # Method: readJson
  # Description: read Json file
  # param: string (filepath)
  # response: json object
  def readJson(json_path):

    # Opening JSON file
    f = open(json_path)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()

    # return data
    return data

#########################################################################################
#########################################################################################

  # Method: parseJson
  # Description: parse Json string
  # param: string (json)
  # response: json object
  def parseJson(jsonData):

    # load JSON object
    data = json.loads(jsonData)

    # return data
    return data

#########################################################################################
#########################################################################################

  ### method: uuid
  ### Description: build uuid value as string
  ### Response: uuid as a string
  def uuid():

    # return
    return str(uuid.uuid4())

#########################################################################################
#########################################################################################

  ### method: randomKeyGenerator
  ### Description: build random key as string
  ### Response: key as a string
  def randomKeyGenerator(size=48, chars=string.ascii_uppercase + string.digits):

    # return
    return ''.join(random.choice(chars) for _ in range(size))

#########################################################################################
#########################################################################################

  ### method: authorize
  ### Description: authorize user with the authorization token & get user details
  ### Response: user + token
  def authorize(token=""):

    # init result
    user = []

    # return - if token is empty
    if(len(token) == 0):
      return user

    # verify token
    jwtToken = []
    if(JwtTokens.objects.filter(jwt_token=token)).exists():
      tokenData = JwtTokens.objects.get(jwt_token=token)
      jwtToken = JwtTokensSerializer(tokenData, many=False)
      jwtToken = jwtToken.data
    else:
      return user

    # fetch user
    if(Users.objects.filter(uuid=jwtToken['user_uuid'])).exists():
      userData = Users.objects.get(uuid=jwtToken['user_uuid'])
      user = UsersSerializer(userData, many=False)
      user = user.data
    else:
      return user

    # add token to user
    user['token'] = token

    # return user details
    return user

#########################################################################################
#########################################################################################
