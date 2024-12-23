from openai import OpenAI
import os
from firebase_functions import https_fn
import json
from typing import Dict, Any
from dotenv import load_dotenv
from pathlib import Path
from prompts import GROUP_QUESTION_PROMPT

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class QuestionGenerator:
    def __init__(self):
        # Initialize OpenAI with API key from environment variable
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=self.api_key)

    def generate_question(self, group_dynamic, interests, previous_questions=None, time_of_day=None, day_of_week=None):
        """
        Generate a contextually appropriate question for a group chat.
        
        Args:
            group_dynamic (str): Description of the group's dynamic
            interests (list): List of group's interests
            previous_questions (list, optional): Recent questions asked to avoid repetition
            time_of_day (str, optional): morning/afternoon/evening
            day_of_week (str, optional): Current day of week
        
        Returns:
            str: Generated question for the group
        """
        group_dynamic_list = group_dynamic if isinstance(group_dynamic, list) else [group_dynamic]
        interests_list = interests if isinstance(interests, list) else [interests]

        completion = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": GROUP_QUESTION_PROMPT.format(
                        group_dynamic=", ".join(group_dynamic_list),
                        interests=", ".join(interests_list),
                        previous_questions=previous_questions or "None",
                        time_of_day=time_of_day or "not specified",
                        day_of_week=day_of_week or "not specified"
                    )
                },
                {
                    "role": "user",
                    "content": "Generate a question for this group."
                }
            ],
            temperature=0.7,  # Add some creativity while maintaining relevance
            max_tokens=100    # Questions should be concise
        )

        return completion.choices[0].message.content.strip()

# # Firebase Cloud Function to generate a question
# @https_fn.on_request()
# def generate_question(req: https_fn.Request) -> https_fn.Response:
#     try:
#         # Get parameters from request
#         topic = req.args.get('topic', 'general knowledge')
#         difficulty = req.args.get('difficulty', 'medium')

#         # Initialize question generator
#         generator = QuestionGenerator()

#         # Generate question
#         question_data = generator.generate_question(topic, difficulty)

#         return https_fn.Response(
#             response=json.dumps({
#                 "success": True,
#                 "data": question_data
#             }),
#             headers={"Content-Type": "application/json"}
#         )

#     except Exception as e:
#         return https_fn.Response(
#             response=json.dumps({
#                 "success": False,
#                 "error": str(e)
#             }),
#             status=500,
#             headers={"Content-Type": "application/json"}
#         )

# # Optional: Function to generate and store question in Firestore
# @https_fn.on_request()
# def generate_and_store_question(req: https_fn.Request) -> https_fn.Response:
#     try:
#         from firebase_admin import firestore

#         # Get parameters
#         topic = req.args.get('topic', 'general knowledge')
#         difficulty = req.args.get('difficulty', 'medium')

#         # Generate question
#         generator = QuestionGenerator()
#         question_data = generator.generate_question(topic, difficulty)

#         # Store in Firestore
#         db = firestore.client()
#         doc_ref = db.collection('questions').document()
#         question_data['created_at'] = firestore.SERVER_TIMESTAMP
#         doc_ref.set(question_data)

#         return https_fn.Response(
#             response=json.dumps({
#                 "success": True,
#                 "data": question_data,
#                 "questionId": doc_ref.id
#             }),
#             headers={"Content-Type": "application/json"}
#         )

#     except Exception as e:
#         return https_fn.Response(
#             response=json.dumps({
#                 "success": False,
#                 "error": str(e)
#             }),
#             status=500,
#             headers={"Content-Type": "application/json"}
#         )
