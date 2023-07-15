# Import libraries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.permissions import AllowAny

import json
import base64
import os
import logging

from .utils import inference_img,inference_text, IMAGE_NAME


def index(request):
    """Render template questionanswering.html for the website UI."""
    return render(request, "qa/questionanswering.html")

class GetAnswers(APIView):
    """
    Create an API (POST method) to response the answer(s)
    for the front-end after running the inference process.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            context = data["context"]
            questions = data["questions"]
            is_image = data["is_image"]

            if(is_image):

                current_directory = os.getcwd()  # Get the current working directory

                image_path = os.path.join(
                    current_directory, IMAGE_NAME
                )  # Construct the absolute path

                """ Decode the string base64 to an image """
                # Remove the 'data:image/jpeg;base64,' prefix and decode the image data
                _, context = context.split(",", 1)
                image_64_decode = base64.b64decode(context)

                # create a writable image and write the decoding result
                image_result = open(image_path, "wb")
                image_result.write(image_64_decode)

                # get the answer from the inference function
                answers = inference_img(image_path, questions)
            
            else:
                print("Inference text")
                answers = inference_text(questions, context)

                
            return Response(
                {"status": "success", "data": answers}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {"status": "error", "data": "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
