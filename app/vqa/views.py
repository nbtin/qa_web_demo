# Import libraries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

import json
import base64
import os
import logging

from .utils import inference, IMAGE_NAME



def index(response):
    """Render template index.html for the website UI."""
    return render(response, "vqa/index.html", {})

# import torch
# from transformers import AutoTokenizer
# from transformers import DistilBertForQuestionAnswering

from transformers import pipeline
question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')


from transformers import DistilBertTokenizer, DistilBertModel
import torch
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')
model = DistilBertModel.from_pretrained('distilbert-base-cased-distilled-squad')




# trained_checkpoint = "distilbert-base-uncased"
# tokenizer = AutoTokenizer.from_pretrained(trained_checkpoint)

# device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
# # Load the saved state dictionary
# current_directory = os.getcwd()  # Get the cSurrent working directory

# model_path = os.path.join(
#     current_directory, "app", "model_v1"
# )  # Construct the absolute path
# state_dict = torch.load("app/vqa/models/model_v1", map_location=device)

# # Create a new instance of the model
# model = DistilBertForQuestionAnswering.from_pretrained(trained_checkpoint)

# # Load the state dictionary into the model
# model.load_state_dict(state_dict)

def predict(text, context):
    
    # inputs = tokenizer(text, context, return_tensors='pt')
    # inputs = {key: val.to(device) for key, val in inputs.items()}

    # with torch.no_grad():
    #     outputs = model(**inputs)
    #     start_logits, end_logits = outputs.start_logits, outputs.end_logits

    # answer_start = torch.argmax(start_logits)
    # answer_end = torch.argmax(end_logits)

    # answer_tokens = inputs["input_ids"][0][answer_start:answer_end+1]
    # answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(answer_tokens))

    return question_answerer(question = text, context = context)["answer"]
    # question, text = "Who was Jim Henson?", "Jim Henson was a nice puppet"

    inputs = tokenizer(text, context, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    return outputs
    

class GetAnswers(APIView):
    """
    Create an API (POST method) to response the answer(s)
    for the front-end after running the inference process.
    """

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            context = data["context"]
            questions = data["questions"]
            is_image = data["is_image"]

            if(is_image):

                current_directory = os.getcwd()  # Get the cSurrent working directory

                image_path = os.path.join(
                    current_directory, "app", IMAGE_NAME
                )  # Construct the absolute path

                """ Decode the string base64 to an image """
                # Remove the 'data:image/jpeg;base64,' prefix and decode the image data
                _, context = context.split(",", 1)
                image_64_decode = base64.b64decode(context)

                # create a writable image and write the decoding result
                image_result = open(image_path, "wb")
                image_result.write(image_64_decode)

                # get the answer from the inference function
                answers = inference(image_path, questions)
            
            else:
                
                answers = predict(context, questions)
                
                
            return Response(
                {"status": "success", "data": answers}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {"status": "error", "data": "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
