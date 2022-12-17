# Import Required stuff
from textblob import TextBlob
from datetime import date
from datetime import datetime

# Import libraries
import os
import uuid
import cv2
import numpy as np
import pytesseract
import datetime

# Processor class
class Processor:

#########################################################################################
#########################################################################################

  ### method: processImage
  ### Description: image segmentation & build data
  ### Params: object (payload)
  ### Response: array of images
  def processImage(payload):

    # Init variables
    result = {
      "image_uuid"      : str(uuid.uuid4()),
      "user_uuid"       : payload['user_uuid'],
      # "created_dt"      : datetime.datetime.now(),
      # "modified_dt"     : datetime.datetime.now(),
      "title"           : payload['title'],
      "description"     : payload['description'] if payload['description'] else "",
      "image"           : 'storage/'+payload['image'],
      "marked_image"    : "",
      "language"        : payload['language'],
      "complete_text"   : Processor.extractTextFromImage('storage/'+payload['image'], payload['language']),
      "status"          : "active",
      "segmentations"   : []
    }

    # create image directory under /storage/processed_images - if does not exist
    processedDirectoryPath = 'storage/processed_images/'+result['image_uuid']
    if(os.path.exists(processedDirectoryPath) == False):
      os.makedirs(processedDirectoryPath)

    # read image
    image = cv2.imread('storage/'+payload['image'])

    # grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    # binary
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)

    # dilation
    kernel = np.ones((5,100), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)

    # find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    for i, ctr in enumerate(sorted_ctrs):
      # Get bounding box
      x, y, w, h = cv2.boundingRect(ctr)

      # Getting ROI
      roi = image[y:y+h, x:x+w]

      # show ROI
      segmentUuid = str(uuid.uuid4())
      segmentImage = 'storage/processed_images/'+result['image_uuid']+'/'+segmentUuid+'.jpg'
      cv2.imwrite(segmentImage, roi)
      cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)

      # push to an array
      result['segmentations'].append({
        "segment_uuid"        : segmentUuid,
        "sequence"            : str(i+1),
        "segment_image"       : segmentImage,
        "segment_text"        : Processor.extractTextFromImage(segmentImage, payload['language']),
        "corrects_count"      : 0,
        "wrongs_count"        : 0,
        "final_text"          : "",
        "status"              : "active",
        "comments"            : [],
        "translations"        : [],
        "word_segmentations"  : []
      })

    # save marked image
    markedImagePath = 'storage/processed_images/'+result['image_uuid']+'/marked_image.jpg'
    cv2.imwrite(markedImagePath, image)
    result['marked_image'] = markedImagePath

    # return
    return result

#########################################################################################
#########################################################################################

  ### method: extractTextFromImage
  ### Description: read text from segmented images
  ### Params: payload (data)
  ### Response: string (extracted text)
  def extractTextFromImage(imagePath, language, to='en', psm='13'):

    # load the input image and convert it from BGR to RGB channel
    # ordering
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # OCR the image, supplying the country code as the language parameter
    options = "-l {} --psm {}".format(language, psm)
    text = pytesseract.image_to_string(rgb, config=options)

    # # translate the text into a different language
    # tb = TextBlob(text)
    # translated = tb.translate(to=args["to"])
    # # show the translated text
    # print("TRANSLATED")
    # print("==========")
    # print(translated)

    # return the extracted text
    return text
