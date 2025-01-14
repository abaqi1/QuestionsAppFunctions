from firebase_functions import https_fn
import json
import uuid
from datetime import datetime
from firebase_admin import firestore
from python.utils.firebase_init import db

@https_fn.on_request()
def generate_test_question(request: https_fn.Request) -> https_fn.Response:
    try:
        # Get group ID from request
        data = request.get_json()
        group_id = data.get('groupId')
        
        if not group_id:
            return https_fn.Response(
                response=json.dumps({
                    "success": False,
                    "error": "Group ID is required"
                }),
                status=400,
                headers={"Content-Type": "application/json"}
            )
        
        
        # Get group data
        group_ref = db.collection('groups').document(group_id)
        group_doc = group_ref.get()
        
        if not group_doc.exists:
            return https_fn.Response(
                response=json.dumps({
                    "success": False,
                    "error": "Group not found"
                }),
                status=404,
                headers={"Content-Type": "application/json"}
            )
        
        # Hardcoded test question
        questions = [
            "What's your favorite memory from the past year?",
            "If you could master any skill instantly, what would it be and why?",
            "What's the best piece of advice you've ever received?",
            "If you could have dinner with anyone from history, who would it be?",
            "What's a small thing that always makes your day better?",
            "What's the most interesting place you've ever visited?",
            "What's a goal you're currently working towards?",
            "What's something you're grateful for today?",
            "If you could live anywhere in the world, where would you choose?",
            "What's a hobby or interest you'd like to explore more?"
        ]

        # Create question objects with unique IDs
        new_questions = [{
            '_id': str(uuid.uuid4()),
            'text': question,
            'createdAt': datetime.utcnow()
        } for question in questions]
        
         # Add questions to next_questions array
        group_ref.update({
            'next_questions': firestore.ArrayUnion(new_questions)
        })
        
        return https_fn.Response(
            response=json.dumps({
                "success": True,
                "data": {
                    "groupId": group_id,
                    "question": new_questions
                }
            }, default=str),
            headers={"Content-Type": "application/json"}
        )
        
    except Exception as e:
        return https_fn.Response(
            response=json.dumps({
                "success": False,
                "error": str(e)
            }),
            status=500,
            headers={"Content-Type": "application/json"}
        )