# Import libraries
from torchvision.transforms.functional import InterpolationMode
from torchvision import transforms
import torch
from PIL import Image
import logging
import os
import base64
# import BLIP model for Visual Question Answering tasks.
from .models.blip_vqa import blip_vqa
from .utils import Utils
IMAGE_NAME = "recently_asked.jpg"

import requests

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-cased-distilled-squad"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


""" Configuration for running the model on GPU cuda if available."""
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

"""
    Define some pre-processing steps to ensure that the input to the model is in the correct format:
        Resizes the input image to a fixed size.
        Converts it to a tensor.
        Normalizes the pixel values to match the mean and standard deviation of the training data. 
"""
image_size = 384
transform = transforms.Compose(
    [
        transforms.Resize(
            (image_size, image_size), interpolation=InterpolationMode.BICUBIC
        ),
        transforms.ToTensor(),
        transforms.Normalize(
            (0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)
        ),
    ]
)


# Download model
model_url = "https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_vqa_capfilt_large.pth"
model = blip_vqa(pretrained=model_url, image_size=image_size, vit="base")
model.eval()
model = model.to(device)



class Model():
    def preprocess_question(self, questions):
        flag = True  # use to check whether the question is a single question (False) or a set of questions (True)

        questions = questions.strip().split("?")
        for i in range(len(questions)):
            questions[i] = questions[i].strip().replace("\n", "")

        while True:
            if "" in questions:
                questions.remove("")
            else:
                break

        if len(questions) == 1:
            flag = False
        else:
            for i in range(len(questions)):
                questions[i] += "?" 

        return flag, questions
    

    def inference(questions, context):
        pass

class ImageModel(Model):
    def inference(self, questions, context):

        current_directory = os.getcwd()  # Get the cSurrent working directory
        image_path = os.path.join(current_directory, IMAGE_NAME)  # Construct the absolute path

        """ Decode the string base64 to an image """
        # Remove the 'data:image/jpeg;base64,' prefix and decode the image data
        _, context = context.split(",", 1)
        image_64_decode = base64.b64decode(context)

        # create a writable image and write the decoding result
        image_result = open(image_path, "wb")
        image_result.write(image_64_decode)

        raw_image = Image.open(image_path)
        image = transform(raw_image).unsqueeze(0).to(device)

        flag, questions = self.preprocess_question(questions)

        answers = (
            ""  # Parameter for saving multiple answers if there are multiple questions.
        )
        with torch.no_grad():
            """Visual Question Answering output"""
            if not flag:
                answer = model(image, questions[0], train=False, inference="generate")
                return answer[0]
            else:
                for quest in questions:
                    answer = model(image, quest, train=False, inference="generate")
                    answers += f"{quest}\n\t&#8594; {answer[0]}.\n\n"
                return answers


class TextModel(Model):

    def query(self, payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def predict(self, question, context):
        output = self.query({
            "inputs": {
                "question": question,
                "context": context
            },
        })
        return output["answer"]

    def inference(self, questions, context):
        flag, questions = self.preprocess_question(questions)
        # print("Preprocess")
        # print(questions)
        # print(context)
        print(flag)
        answers = (
            ""  # Parameter for saving multiple answers if there are multiple questions.
        )
        if not flag:
                answer = self.predict(questions[0], context)
                print(answer)
                return answer
        else:
            for quest in questions:
                answer = self.predict(quest, context)
                answers += f"{quest}\n\t&#8594; {answer}.\n\n"
            return answers