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
        new_question = "What's your favorite memory from the past year?"
        
        # Add question to next_questions array
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