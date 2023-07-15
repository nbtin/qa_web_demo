import base64


class Utils:
    @staticmethod
    def image_to_base64(self, image_path):
        """
        This function takes an image file path as input, encodes the image as a base64 string, and returns
        the encoded string in utf-8 format.

        Args:
            image_path: The file path of the image that needs to be converted to base64 encoding
        Return:
            a base64 encoded string representation of the image located at the specified `image_path`.
        """
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode("utf-8")


# def preprocess_question(questions):
#     """
#     This function pre-processes a string of questions by splitting them into individual questions and
#     removing unnecessary characters.

#     Args:
#         questions: It is expected to be a string containing one or more questions separated by a question mark (?)

#     Return:
#         A tuple containing:
#             flag: a boolean value indicating whether the input string contains a single question or a set of questions.
#             questions: a list of preprocessed questions.
#     """

#     flag = True  # use to check whether the question is a single question (False) or a set of questions (True)

#     questions = questions.strip().split("?")
#     for i in range(len(questions)):
#         questions[i] = questions[i].strip().replace("\n", "")

#     while True:
#         if "" in questions:
#             questions.remove("")
#         else:
#             break

#     if len(questions) == 1:
#         flag = False
#     else:
#         for i in range(len(questions)):
#             questions[i] += "?"

#     return flag, questions


# def inference_img(image_path, questions):
#     """
#     This function takes an image path and a string of question as input, processes the question,
#     and returns the answer(s) using a pre-trained model (BLIP) for visual question answering.

#     Args:
#         image_path: The file path of the image that will be used for visual question answering
#         question: The question to be asked about the image

#     Return:
#         If the question is a single question, it returns the answer to that question.
#         If the question is a set of questions, it returns the answers to all the questions in the set.
#     """

#     # Load image from image_path and pre-process it
#     raw_image = Image.open(image_path)
#     image = transform(raw_image).unsqueeze(0).to(device)

#     flag, questions = preprocess_question(questions)

#     answers = (
#         ""  # Parameter for saving multiple answers if there are multiple questions.
#     )
#     with torch.no_grad():
#         """Visual Question Answering output"""
#         if not flag:
#             answer = model(image, questions[0], train=False, inference="generate")
#             return answer[0]
#         else:
#             for quest in questions:
#                 answer = model(image, quest, train=False, inference="generate")
#                 answers += f"{quest}\n\t&#8594; {answer[0]}.\n\n"
#             return answers


# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()

# def predict(question, context):

#     output = query({
# 	    "inputs": {
# 		    "question": question,
# 		    "context": context
# 	    },
#     })
#     return output["answer"]

# def inference_text(questions, context):
#     flag, questions = preprocess_question(questions)
#     print("Preprocess")
#     print(questions)
#     print(context)

#     answers = (
#         ""  # Parameter for saving multiple answers if there are multiple questions.
#     )
#     if not flag:
#             answer = predict(questions[0], context)
#             print(answer)
#             return answer
#     else:
#         for quest in questions:
#             answer = predict(quest, context)
#             answers += f"{quest}\n\t&#8594; {answer}.\n\n"
#         return answers
