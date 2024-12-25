from firebase_functions import https_fn
import json
import uuid
from datetime import datetime
from firebase_admin import firestore
from python.utils.firebase_init import db

@https_fn.on_request()
def add_message(request: https_fn.Request) -> https_fn.Response:
    try:
        # Get data from request
        data = request.get_json()
        group_id = data.get('groupId')
        message_text = data.get('message')
        sender_id = data.get('senderId')
        
        # Validate required fields
        if not all([group_id, message_text, sender_id]):
            return https_fn.Response(
                response=json.dumps({
                    "success": False,
                    "error": "Missing required fields: groupId, message, and senderId are required"
                }),
                status=400,
                headers={"Content-Type": "application/json"}
            )
        
        db = firestore.client()
        
        # Generate a UUID for the message
        message_id = str(uuid.uuid4())

        # Create message document with timestamp
        message_data = {
            "_id": message_id,
            "text": message_text,
            "user": {
                "_id": sender_id
            },
            "createdAt": datetime.utcnow()
        }
        
        # First update the messages array
        group_ref = db.collection('groups').document(group_id)
        group_ref.update({
            'messages': firestore.ArrayUnion([message_data])
        })
        
        return https_fn.Response(
            response=json.dumps({
                "success": True,
                "data": {
                    "messageId": message_id,
                    "groupId": group_id
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