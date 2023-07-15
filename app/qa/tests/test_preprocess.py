from rest_framework.test import APIClient, APITestCase
from qa.utils import preprocess_question


class PreprocessQuestionTestCase(APITestCase):
    def template_single(self, questions):
        # create a request body with a single question
        request_body = {
            "questions": questions,
        }

        # preprocess the questions
        flag, result = preprocess_question(request_body["questions"])

        # check if the flag is False (indicating a single question)
        self.assertFalse(flag)

        # check if the questions list contains only one question
        self.assertEqual(len(result), 1)

        # check if the preprocessed question is the expected value
        self.assertEqual(result[0], questions[:-1])

    def template_multiple(self, questions, questions_list):
        # create a request body with multiple questions
        request_body = {
            "questions": questions,
        }

        # preprocess the questions
        flag, result = preprocess_question(request_body["questions"])

        # check if the flag is True (indicating multiple questions)
        self.assertTrue(flag)

        # check if the questions list contains the expected number of questions
        self.assertEqual(len(result), len(questions_list))

        # check if the preprocessed questions are the expected values
        for i in range(len(result)):
            self.assertEqual(result[i], questions_list[i])

    def test_preprocess_single_question_1(self):
        questions = "what is the color of their kit?"
        self.template_single(questions)

    def test_preprocess_multiple_question_1(self):
        questions = "how many people are there???\n\n what is the number on his back  ? \n\n what is the color of their kit  ??"
        questions_list = [
            "how many people are there?",
            "what is the number on his back?",
            "what is the color of their kit?",
        ]
        self.template_multiple(questions, questions_list)

    def test_preprocess_multiple_question_2(self):
        questions = "\n\n ?? ? what is the color of the woman's shirt \n\n ? ?? ? what is the color of the man's shirt??  what is the type of vehicle? \nwhat is the biggest number on the screen\n\n???"
        questions_list = [
            "what is the color of the woman's shirt?",
            "what is the color of the man's shirt?",
            "what is the type of vehicle?",
            "what is the biggest number on the screen?",
        ]
        self.template_multiple(questions, questions_list)
