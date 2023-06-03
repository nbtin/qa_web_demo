import json
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
# from vqa.views import GetAnswers
from vqa.utils import preprocess_question, image_to_base64
import base64
import os

class GetAnswersTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def template(self, questions, image_name, answers):
        # create a valid request body
        request_body = {
            "questions": questions,
        }

        # Remove the 'data:image/jpeg;base64,' prefix
        image = image_to_base64(os.path.join(os.getcwd(), 'app', 'vqa', 'tests', 'imgs', image_name))

        request_body["image"] = 'data:image/jpeg;base64,' + image
        
        # make the API call
        response = self.client.post('/answer', json.dumps(request_body), content_type='application/json')

        # check if the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if the response contains "status" and "data" keys
        self.assertIn("status", response.data)
        self.assertIn("data", response.data)

        # check if the "status" key has the value "success"
        self.assertEqual(response.data["status"], "success")

        # check if the "data" key contains the expected answer(s)
        for answer in answers:
            self.assertIn(answer, response.data["data"])


    def test_get_answers_1(self):
        questions = "how many people are there? what is the number on his back? what is the color of their kit?"
        answers = ["2.", "7.", "white."]
        self.template(questions, 'image1.jpg', answers)
    
    def test_get_answers_2(self):
        questions = "what is the color of the woman\'s shirt? what is the color of the man\'s shirt? what is the type of vehicle? what is the biggest number on the screen?"
        answers = ["black.", "yellow.", "jeep.", "55."]
        self.template(questions, 'image2.jpg', answers)


class PreprocessQuestionTestCase(APITestCase):
    def test_preprocess_single_question(self):
        # create a request body with a single question
        request_body = {
            "questions": "what is the color of their kit?"
        }

        # preprocess the questions
        flag, questions = preprocess_question(request_body["questions"])

        # check if the flag is False (indicating a single question)
        self.assertFalse(flag)

        # check if the questions list contains only one question
        self.assertEqual(len(questions), 1)

        # check if the preprocessed question is the expected value
        self.assertEqual(questions[0], "what is the color of their kit")

    def test_preprocess_multiple_questions(self):
        # create a request body with multiple questions
        request_body = {
            "questions": "how many people are there???\n\n what is the number on his back  ? \n\n what is the color of their kit  ??"
        }

        # preprocess the questions
        flag, questions = preprocess_question(request_body["questions"])

        # check if the flag is True (indicating multiple questions)
        self.assertTrue(flag)

        # check if the questions list contains the expected number of questions
        self.assertEqual(len(questions), 3)

        # check if the preprocessed questions are the expected values
        self.assertEqual(questions[0], "how many people are there?")
        self.assertEqual(questions[1], "what is the number on his back?")
        self.assertEqual(questions[2], "what is the color of their kit?")