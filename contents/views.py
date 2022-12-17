# Import from Django
from django.core import serializers

# Import from Rest Frameworks
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Import serializers
from .serializers import ImagesSerializer

# Import models
from .models import Images

# Import Utilities
from app.utils.utils import Utils
from app.utils.mongo import Mongo
from app.utils.processor import Processor

###
## Create your views here
###

### GET - FETCH CONTENTS ENDPOINT ###
@api_view(['GET'])
def fetch(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # create mongo connection & get collection
  collection = Mongo.mongo_conn('ocr_contents')

  # Parameters (uuid, user_uuid, status)
  params = {}
  if(request.GET.get('uuid')):
    params['image_uuid'] = request.GET.get('uuid')
  if(request.GET.get('user_uuid')):
    params['user_uuid'] = request.GET.get('user_uuid')
  if(request.GET.get('status')):
    params['status'] = request.GET.get('status')

  # find record with id = 1
  fetchData = collection.find(params)

  # parse mongo response
  data = Mongo.parseMongoData(fetchData, True)

  # return response
  return Response(Utils.successResponse(data))

#########################################################################################
#########################################################################################

### POST - CREATE CONTENTS ENDPOINT ###
@api_view(['POST'])
def create(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # payload
  payload = Utils.parseJson(request.body)

  # verify required fields exist
  verifyFields = Utils.verifyFields(payload, ['user_uuid','title','image','language'])
  if(len(verifyFields) > 0):
    return Response(Utils.errorResponse(verifyFields, "Bad Request"), 400)

  # mandatory fields check
  mandatoryFields = Utils.mandatoryFields(payload, ['user_uuid','title','image','language'])
  if(len(mandatoryFields) > 0):
    return Response(Utils.errorResponse(mandatoryFields, "Bad Request"), 400)

  # process the image
  contentData = Processor.processImage(payload)

  # build data to save record in DB
  mysqlDbBody = {
    "uuid"        : contentData['image_uuid'],
    "user_uuid"   : contentData['user_uuid'],
    "title"       : contentData['title'],
    "description" : contentData['description'],
    "image"       : contentData['image'],
    "language"    : contentData['language'],
    "status"      : contentData['status'],
    "created_dt"  : "2022-01-01",
    "modified_dt" : "2022-01-01",
  }

  # save record in MYSQL DB
  serializer = ImagesSerializer(data=mysqlDbBody)
  if serializer.is_valid():
    serializer.save()
  else:
    return Response(Utils.errorResponse({}), 500)

  # create mongo connection & get collection
  collection = Mongo.mongo_conn('ocr_contents')

  # save record in MONGO DB
  insertData = collection.insert_one(contentData)

  # return response
  return Response(Utils.successResponse({"uuid": contentData['image_uuid']}, "Image processed successfully!"))

#########################################################################################
#########################################################################################

### POST - CREATE SEGMENTATION COMMENTS ENDPOINT ###
# Expected Payload
# {
#   "content_uuid": "",
#   "segment_uuid": "",
#   "user_vote": "",
#   "user_text": ""
# }
###
@api_view(['POST'])
def createSegmentationComment(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # payload
  payload = Utils.parseJson(request.body)

  # verify required fields exist
  verifyFields = Utils.verifyFields(payload, ['content_uuid','segment_uuid','user_vote','user_text'])
  if(len(verifyFields) > 0):
    return Response(Utils.errorResponse(verifyFields, "Bad Request"), 400)

  # mandatory fields check
  mandatoryFields = Utils.mandatoryFields(payload, ['content_uuid','segment_uuid','user_vote'])
  if(len(mandatoryFields) > 0):
    return Response(Utils.errorResponse(mandatoryFields, "Bad Request"), 400)

  # make sure user_vote is correct/wrong
  if(payload['user_vote'] != 'correct' and payload['user_vote'] != 'wrong'):
    return Response(Utils.errorResponse("user_vote must be either correct/wrong", "Bad Request"), 400)

  # create mongo connection & get collection
  collection = Mongo.mongo_conn('ocr_contents')

  ####
  ##  ADD COMMENT
  ###

  # build query
  myQuery = {
    "image_uuid": payload['content_uuid'],
    "segmentations.segment_uuid": payload['segment_uuid']
  }

  # create modified data
  commentData = {
    "segmentations.$.comments": {
      "comment_uuid": Utils.uuid(),
      "user_uuid": authorize['uuid'],
      "user_vote": payload['user_vote'],
      "user_text": payload['user_text']
    }
  }

  # find & modify
  collection.find_one_and_update(myQuery,{"$push":commentData})

  # fetch content & parse response
  fetchContent = collection.find({"image_uuid":payload['content_uuid']})
  fetchContent = Mongo.parseMongoData(fetchContent, False)

  # correct/wrong data
  corrects_count = 0
  wrongs_count = 0
  if(payload['user_vote'] == 'correct'):
    corrects_count = int(corrects_count) + int(1)
  else:
    wrongs_count = int(wrongs_count) + int(1)

  # find appropriate segmentation
  # get correct/wrong counts
  segmentation = {}
  for segment in fetchContent['segmentations']:
    if segment['segment_uuid'] == payload['segment_uuid']:
      segmentation = segment
      for comment in segment['comments']:
        if comment['user_vote'] == "correct":
          corrects_count = int(corrects_count) + int(1)
        if comment['user_vote'] == "wrong":
          wrongs_count = int(wrongs_count) + int(1)
      break

  ####
  ##  UPDATE CORRECT/WRONG COUNT
  ###

  # build query
  myQuery = {
    "image_uuid": payload['content_uuid'],
    "segmentations.segment_uuid": payload['segment_uuid']
  }

  # correct/wrong data
  countData = {
    'segmentations.$.corrects_count': corrects_count,
    'segmentations.$.wrongs_count': wrongs_count
  }

  # find & modify
  collection.find_one_and_update(myQuery,{"$set":countData})

  # return response
  return Response(Utils.successResponse(segmentation, "Comment added successfully!"))

#########################################################################################
#########################################################################################

### POST - CREATE SEGMENTATION COMMENTS ENDPOINT ###
# Expected Payload
# {
#   "content_uuid": "",
#   "segment_uuid": "",
#   "comment_uuid": "",
#   "user_vote": "",
#   "user_text": ""
# }
###
@api_view(['PUT'])
def updateSegmentationComment(request):

  # authorize user
  authorize = Utils.authorize(request.headers['Authorization'])
  if(len(authorize) == 0):
    return Response(Utils.errorResponse("Invalid authorization token", "UnAuthorized"), 401)

  # payload
  payload = Utils.parseJson(request.body)

  # verify required fields exist
  verifyFields = Utils.verifyFields(payload, ['content_uuid','segment_uuid','comment_uuid','user_vote','user_text'])
  if(len(verifyFields) > 0):
    return Response(Utils.errorResponse(verifyFields, "Bad Request"), 400)

  # mandatory fields check
  mandatoryFields = Utils.mandatoryFields(payload, ['content_uuid','segment_uuid','comment_uuid','user_vote'])
  if(len(mandatoryFields) > 0):
    return Response(Utils.errorResponse(mandatoryFields, "Bad Request"), 400)

  # make sure user_vote is correct/wrong
  if(payload['user_vote'] != 'correct' and payload['user_vote'] != 'wrong'):
    return Response(Utils.errorResponse("user_vote must be either correct/wrong", "Bad Request"), 400)

  # create mongo connection & get collection
  collection = Mongo.mongo_conn('ocr_contents')

  ####
  ##  UPDATE COMMENT
  ###

  # build query
  myQuery = {
    "image_uuid": payload['content_uuid']
  }

  # create modified data
  commentData = {
    "segmentations.$[i].comments.$[j].user_vote": payload['user_vote'],
    "segmentations.$[i].comments.$[j].user_text": payload['user_text']
  }

  # find & modify
  collection.find_one_and_update(myQuery,{"$set":commentData}, array_filters = [
      { "i.segment_uuid": payload['segment_uuid'] },
      { "j.comment_uuid": payload['comment_uuid'] }
    ]
  )

  # fetch content & parse response
  fetchContent = collection.find({"image_uuid":payload['content_uuid']})
  fetchContent = Mongo.parseMongoData(fetchContent, False)

  # correct/wrong data
  corrects_count = 0
  wrongs_count = 0
  if(payload['user_vote'] == 'correct'):
    corrects_count = int(corrects_count) + int(1)
  else:
    wrongs_count = int(wrongs_count) + int(1)

  # find appropriate segmentation
  # get correct/wrong counts
  segmentation = {}
  for segment in fetchContent['segmentations']:
    if segment['segment_uuid'] == payload['segment_uuid']:
      segmentation = segment
      for comment in segment['comments']:
        if comment['user_vote'] == "correct":
          corrects_count = int(corrects_count) + int(1)
        if comment['user_vote'] == "wrong":
          wrongs_count = int(wrongs_count) + int(1)
      break

  ####
  ##  UPDATE CORRECT/WRONG COUNT
  ###

  # build query
  myQuery = {
    "image_uuid": payload['content_uuid'],
    "segmentations.segment_uuid": payload['segment_uuid']
  }

  # correct/wrong data
  countData = {
    'segmentations.$.corrects_count': corrects_count,
    'segmentations.$.wrongs_count': wrongs_count
  }

  # find & modify
  collection.find_one_and_update(myQuery,{"$set":countData})

  # return response
  return Response(Utils.successResponse(segmentation, "Comment updated successfully!"))

#########################################################################################
#########################################################################################
