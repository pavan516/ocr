# Import Utilities
from .utils import Utils
from bson import json_util

# Import os, pymongo, json
import os
import pymongo
import json

# Mongo class
class Mongo:

#########################################################################################
#########################################################################################

  # Method: mongo connection
  # Description: Create mongo connection
  def mongo_conn(collectionName):

    # get json path
    json_path = os.getcwd()+'/app/config/config.json'

    # read json file
    config = Utils.readJson(json_path)

    # create client
    client = pymongo.MongoClient(config['mongo_host'])

    # Database Name
    db = client[config['mongo_db']]

    # return collection
    return db[collectionName]

#########################################################################################
#########################################################################################

  # Method: parseMongoData
  # Description: Parse mongo data & return proper response
  # params: array (data), string many (true/false)
  # response: json object
  def parseMongoData(data, many=True):

    # consider data based on many check
    if(many):
      # Init result
      result = []
      # make sure we have data
      if(data.count() == 0):
        return result
      # loop data
      for item in data:
        # let's dump data
        dumpData = json.dumps(item, default=json_util.default)
        # parse dumped data
        parsedData = Utils.parseJson(dumpData)
        # remove _id key if exist
        if "_id" in parsedData:
          del parsedData['_id']
        # push to an array
        result.append(parsedData)
    else:
      # Init result
      result = {}
      # make sure we have data
      if(data.count() == 0):
        return result
      # let's dump data
      dumpData = json.dumps(data[0], default=json_util.default)
      # parse dumped data
      parsedData = Utils.parseJson(dumpData)
      # remove _id key if exist
      if "_id" in parsedData:
        del parsedData['_id']
      # push to result
      result = parsedData

    # return
    return result

#########################################################################################
#########################################################################################
