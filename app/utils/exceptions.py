# Import from rest_framework
from rest_framework.views import exception_handler
from rest_framework.response import Response

# Method: custom_exception_handler
# Description: Custom exception handler
def custom_exception_handler(exc, context):

  # get response
  response = exception_handler(exc, context)

  # return response, if response is none
  if response is not None:
    return response

  # get details by splitting error response
  exc_list = str(exc).split("DETAIL: ")

  # Build error response
  error = {
    "status": "error",
    "code": 0,
    "message": "Something went wrong",
    "details": exc_list[-1]
  }

  # return response
  return Response(error, status=500)