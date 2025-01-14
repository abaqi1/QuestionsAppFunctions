from firebase_functions import https_fn
import json
import uuid
from datetime import datetime
from firebase_admin import firestore, messaging
from python.utils.firebase_init import db

@https_fn.on_request()
def post_next_question(request: https_fn.Request) -> https_fn.Response:
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
        
        db = firestore.client()
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
        next_questions = group_data.get('next_questions', [])
        group_name = group_data.get('name', '')
        
        # Check if there are any questions in the queue
        if not next_questions:
            return https_fn.Response(
                response=json.dumps({
                    "success": False,
                    "error": "No questions in queue"
                }),
                status=404,
                headers={"Content-Type": "application/json"}
            )
        
        # Get the first question
        next_question = next_questions[0]
        remaining_questions = next_questions[1:]
        
        # Create message data for the question
        message_data = {
            "_id": str(uuid.uuid4()),
            "text": next_question['text'],
            "user": {
                "_id": "SYSTEM"  # or whatever ID you want to use for system messages
            },
            "createdAt": datetime.utcnow()
        }
        
        # Update the document in a transaction to ensure atomicity
        @firestore.transactional
        def update_in_transaction(transaction, group_ref):
            # Add to messages array and update next_questions array
            transaction.update(group_ref, {
                'messages': firestore.ArrayUnion([message_data]),
                'next_questions': remaining_questions
            })
        
        # Run the transaction
        transaction = db.transaction()
        update_in_transaction(transaction, group_ref)
        
                # After successful transaction, send notification to all iOS users
        try:
            
            # Define the message payload
            message = messaging.Message(
                notification=messaging.Notification(
                    title=group_name,
                    body=next_question['text']
                ),
                token="USER_TOKEN_HERE"
            )

            # Send the message
            response = messaging.send(message)
            print('Successfully sent message:', response)
        except Exception as e:
            print('Error sending notification:', str(e))
        


        return https_fn.Response(
            response=json.dumps({
                "success": True,
                "data": {
                    "messageId": message_data["_id"],
                    "groupId": group_id,
                    "question": message_data["text"],
                    "remainingQuestions": len(remaining_questions)
                }
            }, default=str),
            headers={"Content-Type": "application/json"}
        )

    # SEND NOTIFICATION TO GRoup Topic 
        
    except Exception as e:
        return https_fn.Response(
            response=json.dumps({
                "success": False,
                "error": str(e)
            }),
            status=500,
            headers={"Content-Type": "application/json"}
        )