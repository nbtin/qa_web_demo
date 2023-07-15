import json
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from vqa.utils import Utils
import os


class GetAnswersTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def template(self, questions, image_name, answers, is_image):
        # create a valid request body
        request_body = {
            "questions": questions,
            "is_image": is_image,
        }

        # Remove the 'data:image/jpeg;base64,' prefix
        image = Utils.image_to_base64(
            os.path.join(os.getcwd(), "app", "vqa", "tests", "imgs", image_name)
        )

        if is_image:
            request_body["context"] = "data:image/jpeg;base64," + image
        else:
            request_body["context"] = ""  # add later

        # make the API call
        response = self.client.post(
            "/qa/answer/", json.dumps(request_body), content_type="application/json"
        )

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
        self.template(questions, "image1.jpg", answers, is_image=True)

    def test_get_answers_2(self):
        questions = "what is the color of the woman's shirt? what is the color of the man's shirt? what is the type of vehicle? what is the biggest number on the screen?"
        answers = ["black.", "yellow.", "jeep.", "55."]
        self.template(questions, "image2.jpg", answers, is_image=True)

    def test_get_answers_3(self):
        questions = "what are they looking at? who is standing? what are they doing?"
        answers = ["laptops.", "woman.", "studying."]
        self.template(questions, "image3.jpg", answers, is_image=True)

    def test_get_answers_4(self):
        questions = "what is on the table? what kind of table is it? who is sitting on the chair? what is the color of the chair? what is he doing? does he have eyes? what did his legs do? what is on his hand? what is the color of the phone?"
        answers = [
            "coffee cup and saucer.",
            "wooden.",
            "skeleton.",
            "blue.",
            "using laptop.",
            "no.",
            "crossed.",
            "phone.",
            "black.",
        ]
        self.template(questions, "image4.jpg", answers, is_image=True)
