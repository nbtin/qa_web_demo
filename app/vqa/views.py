# Import libraries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

import json
import base64
import os
import logging

from .utils import Utils
from .model import Model, ImageModel, TextModel



def index(response):
    """Render template index.html for the website UI."""
    return render(response, "vqa/index.html", {})
class GetAnswers(APIView):
    """
    Create an API (POST method) to response the answer(s)
    for the front-end after running the inference process.
    """
    def __init__(self):
        self.model = Model()
    
    def set_model(self, model):
        self.model = model

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            context = data["context"]
            questions = data["questions"]
            is_image = data["is_image"]

            if(is_image):
                self.set_model(ImageModel())
            else:
                self.set_model(TextModel())
                
            answer = self.model.inference(questions, context)
            return answer

        except Exception as e:
            print(e)
            return Response(
                {"status": "error", "data": "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
