from firebase_functions import https_fn
import json
import uuid
from datetime import datetime
from firebase_admin import firestore
from python.utils.firebase_init import db

@https_fn.on_request()
def generate_group_question(request: https_fn.Request) -> https_fn.Response:
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
        
        group_data = group_doc.to_dict()
        
        # Get group interests and dynamics
        interests = group_data.get('interests', [])
        dynamics = group_data.get('dynamics', [])
        
        # Get previous questions to avoid repetition
        previous_questions = [msg.get('text') for msg in group_data.get('messages', []) 
                            if msg.get('text')]
        
        # Generate new question
        from functions.python.agent.question_agent import QuestionGenerator
        generator = QuestionGenerator()
        
        new_question = generator.generate_question(
            group_dynamic=dynamics,
            interests=interests,
            previous_questions=previous_questions
        )
        
        # Add question to next_questions array
        if 'next_questions' not in group_data:
            group_ref.update({'next_questions': []})
        
        group_ref.update({
            'next_questions': firestore.ArrayUnion([{
                '_id': str(uuid.uuid4()),
                'text': new_question,
                'createdAt': datetime.utcnow()
            }])
        })
        
        return https_fn.Response(
            response=json.dumps({
                "success": True,
                "data": {
                    "groupId": group_id,
                    "question": new_question
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