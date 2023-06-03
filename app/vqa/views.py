# Import libraries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
from django.shortcuts import render
from datetime import datetime
# from django.http import HttpResponse

import json
import torch
import base64
import os

from rest_framework.parsers import JSONParser
IMAGE_NAME = 'recently_asked.jpg'

from .models.blip import blip_decoder
from .models.blip_vqa import blip_vqa
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode

# Download model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

image_size = 384
transform = transforms.Compose([
    transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
    transforms.ToTensor(),
    transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
    ]) 

model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_vqa_capfilt_large.pth'

model = blip_vqa(pretrained=model_url, image_size=image_size, vit='base')
model.eval()
model = model.to(device)

def index(response):
    return render(response, "vqa/index.html", {})

def inference(image_path, question):
    flag = True
    raw_image = Image.open(image_path)
    image = transform(raw_image).unsqueeze(0).to(device)   
    questions = question.strip().split('?')
    for i in range(len(questions)): questions[i] = questions[i].strip().replace('\n', '')
    while True: 
        if '' in questions: 
            questions.remove('')
        else:
            break
    if len(questions) == 1:
        flag = False
    else:
        for i in range(len(questions)):
            questions[i] += '?'
    answers = ''
    with torch.no_grad():
        ''' Visual Question Answering output '''
        if not flag:
            answer = model(image, question, train=False, inference='generate')
            return answer[0]
        else:
            for quest in questions:
                answer = model(image, quest, train=False, inference='generate')
                answers += f'{quest}\n\t&#8594; {answer[0]}.\n\n'
            return answers

class GetAnswers(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            image = data['image']
            questions = data['questions']
            
            current_directory = os.getcwd()  # Get the current working directory
            
            image_path = os.path.join(current_directory, 'app', IMAGE_NAME)  # Construct the absolute path

            # decode the string base64 to an image
            _, image = image.split(',', 1)  # Remove the 'data:image/jpeg;base64,' prefix
            image_64_decode = base64.b64decode(image) 
            image_result = open(image_path, 'wb') # create a writable image and write the decoding result
            image_result.write(image_64_decode)

            ans = inference(image_path, questions)

            return Response({"status": "success", "data": ans}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"status": "error", "data": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
