# Import libraries
import torch
import gradio as gr

from models.blip import blip_decoder
from models.blip_vqa import blip_vqa
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

# image captioning
# model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_large_caption.pth'
# visual question answering
model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_vqa_capfilt_large.pth'

model = blip_vqa(pretrained=model_url, image_size=image_size, vit='base')
model.eval()
model = model.to(device)

# Deploy
title       = 'Visual Question Answering'
description = '''
              '''
# inputs      = gr.inputs.Image(type='pil')
inputs      = [gr.inputs.Image(type='pil'), gr.Text()]
# question = gr.inputs.Text()
outputs     = gr.outputs.Textbox(label='Output')

def inference(raw_image, question):
    flag = True
    image = transform(raw_image).unsqueeze(0).to(device)   
    questions = question.split('?')
    for i in range(len(questions)): questions[i].strip()
    questions.remove('')
    if len(questions) == 1:
        flag = False
    else:
        for i in range(len(questions)):
            questions[i] += '?'
    answers = ''
    with torch.no_grad():
        ''' Image captioning output '''
        # caption = model.generate(image, sample=False, num_beams=3, max_length=20, min_length=5)
        # return caption[0]
        ''' Visual Question Answering output '''
        if not flag:
            answer = model(image, question, train=False, inference='generate')
            return answer[0]
        else:
            for quest in questions:
                answer = model(image, quest, train=False, inference='generate')
                answers += f'QUESTION: {quest}  ===>  ANSWER: {answer[0]}.\n'
            return answers


gr.Interface(inference, inputs, outputs, title=title, description=description).launch(enable_queue=True, share='True')