# # Welcome to Cloud Functions for Firebase for Python!
# # To get started, simply uncomment the below code or create your own.
# # Deploy with `firebase deploy`

# from firebase_functions import https_fn, options
# import firebase_admin
# from firebase_admin import firestore, initialize_app
# import json
# import os
# from config.firebase_config import FIREBASE_CONFIG
# import uuid
# from datetime import datetime
# # from google.cloud.firestore_v1.transforms import Timestamp


# # Initialize Firebase Admin
# # Environment variable to control emulator usage
# USE_EMULATOR = os.getenv('USE_EMULATOR', 'false').lower() == 'true'

# config = FIREBASE_CONFIG['emulator'] if USE_EMULATOR else FIREBASE_CONFIG['cloud']

# if USE_EMULATOR:
#     os.environ["FIRESTORE_EMULATOR_HOST"] = config['firestore_host']
#     os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = config['auth_host']
#     firebase_admin.initialize_app(options={'projectId': config['projectId']})
# else:
#     # cred = credentials.Certificate(config['credentials_path'])
#     # firebase_admin.initialize_app(cred, {'projectId': config['projectId']})
#     initialize_app()

# # @https_fn.on_request()
# # def get_groups(request: https_fn.Request) -> https_fn.Response:
# #     try:
# #         db = firestore.client()
# #         if USE_EMULATOR:
# #             print("Using Firestore emulator at:", os.getenv("FIRESTORE_EMULATOR_HOST"))
# #         else:
# #             print("Using Cloud Firestore")
        
# #         groups_ref = db.collection('groups')
# #         docs = groups_ref.stream()
        
# #         groups = []
# #         for doc in docs:
# #             group_data = doc.to_dict()
# #             group_data['id'] = doc.id
# #             groups.append(group_data)
        
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": True,
# #                 "data": groups,
# #                 "count": len(groups),
# #                 "mode": "emulator" if USE_EMULATOR else "cloud",
# #                 "emulator_host": os.getenv("FIRESTORE_EMULATOR_HOST") if USE_EMULATOR else None
# #             }, default=str),
# #             headers={"Content-Type": "application/json"}
# #         )
# #     except Exception as e:
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": False,
# #                 "error": str(e),
# #                 "mode": "emulator" if USE_EMULATOR else "cloud"
# #             }),
# #             status=500,
# #             headers={"Content-Type": "application/json"}
# #         )

# # @https_fn.on_request()
# # def get_users(request: https_fn.Request) -> https_fn.Response:
# #     try:
# #         print("Connecting to Firestore emulator at:", os.getenv("FIRESTORE_EMULATOR_HOST"))
# #         group_id = request.args.get('groupId')
# #         limit = int(request.args.get('limit', '10'))
        
# #         db = firestore.client()
# #         users_ref = db.collection('users')
        
# #         if group_id:
# #             users_ref = users_ref.where('groupId', '==', group_id)
        
# #         docs = users_ref.limit(limit).stream()
        
# #         users = []
# #         for doc in docs:
# #             user_data = doc.to_dict()
# #             user_data['id'] = doc.id
# #             users.append(user_data)
        
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": True,
# #                 "data": users,
# #                 "count": len(users),
# #                 "filters": {
# #                     "groupId": group_id,
# #                     "limit": limit
# #                 },
# #                 "emulator": os.getenv("FIRESTORE_EMULATOR_HOST")
# #             }),
# #             headers={"Content-Type": "application/json"}
# #         )
# #     except Exception as e:
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": False,
# #                 "error": str(e),
# #                 "emulator": os.getenv("FIRESTORE_EMULATOR_HOST")
# #             }),
# #             status=500,
# #             headers={"Content-Type": "application/json"}
# #         )

# # # Get a specific group by ID
# # @https_fn.on_request()
# # def get_group(request: https_fn.Request) -> https_fn.Response:
# #     try:
# #         group_id = request.args.get('id')
# #         if not group_id:
# #             return https_fn.Response(
# #                 response=json.dumps({
# #                     "success": False,
# #                     "error": "Group ID is required"
# #                 }),
# #                 status=400,
# #                 headers={"Content-Type": "application/json"}
# #             )
        
# #         db = firestore.client()
# #         doc = db.collection('groups').document(group_id).get()
        
# #         if not doc.exists:
# #             return https_fn.Response(
# #                 response=json.dumps({
# #                     "success": False,
# #                     "error": "Group not found"
# #                 }),
# #                 status=404,
# #                 headers={"Content-Type": "application/json"}
# #             )
        
# #         group_data = doc.to_dict()
# #         group_data['id'] = doc.id
        
# #         # Get users in this group
# #         users_ref = db.collection('users').where('groupId', '==', group_id).stream()
# #         users = []
# #         for user_doc in users_ref:
# #             user_data = user_doc.to_dict()
# #             user_data['id'] = user_doc.id
# #             users.append(user_data)
        
# #         group_data['users'] = users
        
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": True,
# #                 "data": group_data
# #             }, default=str),
# #             headers={"Content-Type": "application/json"}
# #         )
# #     except Exception as e:
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": False,
# #                 "error": str(e)
# #             }),
# #             status=500,
# #             headers={"Content-Type": "application/json"}
# #         )
    
# # @https_fn.on_request()
# # def add_message(request: https_fn.Request) -> https_fn.Response:
# #     try:
# #         # Get data from request
# #         data = request.get_json()
# #         group_id = data.get('groupId')
# #         message_text = data.get('message')
# #         sender_id = data.get('senderId')
        
# #         # Validate required fields
# #         if not all([group_id, message_text, sender_id]):
# #             return https_fn.Response(
# #                 response=json.dumps({
# #                     "success": False,
# #                     "error": "Missing required fields: groupId, message, and senderId are required"
# #                 }),
# #                 status=400,
# #                 headers={"Content-Type": "application/json"}
# #             )
        
# #         db = firestore.client()
        
# #         # Generate a UUID for the message
# #         message_id = str(uuid.uuid4())

# #         # Create message document with timestamp
# #         message_data = {
# #             "_id": message_id,
# #             "text": message_text,
# #             "user": {
# #                 "_id": sender_id
# #             },
# #             "createdAt": datetime.utcnow()
# #         }
        
# #         # First update the messages array
# #         group_ref = db.collection('groups').document(group_id)
# #         group_ref.update({
# #             'messages': firestore.ArrayUnion([message_data])
# #         })
        
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": True,
# #                 "data": {
# #                     "messageId": message_id,
# #                     "groupId": group_id
# #                 }
# #             }, default=str),
# #             headers={"Content-Type": "application/json"}
# #         )
        
# #     except Exception as e:
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": False,
# #                 "error": str(e)
# #             }),
# #             status=500,
# #             headers={"Content-Type": "application/json"}
# #         )
    
# # @https_fn.on_request()
# # def generate_group_question(request: https_fn.Request) -> https_fn.Response:
# #     try:
# #         # Get group ID from request
# #         data = request.get_json()
# #         group_id = data.get('groupId')
        
# #         if not group_id:
# #             return https_fn.Response(
# #                 response=json.dumps({
# #                     "success": False,
# #                     "error": "Group ID is required"
# #                 }),
# #                 status=400,
# #                 headers={"Content-Type": "application/json"}
# #             )
        
# #         db = firestore.client()
        
# #         # Get group data
# #         group_ref = db.collection('groups').document(group_id)
# #         group_doc = group_ref.get()
        
# #         if not group_doc.exists:
# #             return https_fn.Response(
# #                 response=json.dumps({
# #                     "success": False,
# #                     "error": "Group not found"
# #                 }),
# #                 status=404,
# #                 headers={"Content-Type": "application/json"}
# #             )
        
# #         group_data = group_doc.to_dict()
        
# #         # Get group interests and dynamics
# #         interests = group_data.get('interests', [])
# #         dynamics = group_data.get('dynamics', [])
        
# #         # Get previous questions to avoid repetition
# #         previous_questions = [msg.get('text') for msg in group_data.get('messages', []) 
# #                             if msg.get('text')]
        
# #         # Generate new question
# #         from question_agent import QuestionGenerator
# #         generator = QuestionGenerator()
        
# #         new_question = generator.generate_question(
# #             group_dynamic=dynamics,
# #             interests=interests,
# #             previous_questions=previous_questions
# #         )
        
# #         # Add question to next_questions array
# #         if 'next_questions' not in group_data:
# #             group_ref.update({'next_questions': []})
        
# #         group_ref.update({
# #             'next_questions': firestore.ArrayUnion([{
# #                 '_id': str(uuid.uuid4()),
# #                 'text': new_question,
# #                 'createdAt': datetime.utcnow()
# #             }])
# #         })
        
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": True,
# #                 "data": {
# #                     "groupId": group_id,
# #                     "question": new_question
# #                 }
# #             }, default=str),
# #             headers={"Content-Type": "application/json"}
# #         )
        
# #     except Exception as e:
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": False,
# #                 "error": str(e)
# #             }),
# #             status=500,
# #             headers={"Content-Type": "application/json"}
# #         )
    
# # @https_fn.on_request()
# # def generate_test_question(request: https_fn.Request) -> https_fn.Response:
# #     try:
# #         # Get group ID from request
# #         data = request.get_json()
# #         group_id = data.get('groupId')
        
# #         if not group_id:
# #             return https_fn.Response(
# #                 response=json.dumps({
# #                     "success": False,
# #                     "error": "Group ID is required"
# #                 }),
# #                 status=400,
# #                 headers={"Content-Type": "application/json"}
# #             )
        
# #         db = firestore.client()
        
# #         # Get group data
# #         group_ref = db.collection('groups').document(group_id)
# #         group_doc = group_ref.get()
        
# #         if not group_doc.exists:
# #             return https_fn.Response(
# #                 response=json.dumps({
# #                     "success": False,
# #                     "error": "Group not found"
# #                 }),
# #                 status=404,
# #                 headers={"Content-Type": "application/json"}
# #             )
        
# #         # Hardcoded test question
# #         new_question = "What's your favorite memory from the past year?"
        
# #         # Add question to next_questions array
# #         group_ref.update({
# #             'next_questions': firestore.ArrayUnion([{
# #                 '_id': str(uuid.uuid4()),
# #                 'text': new_question,
# #                 'createdAt': datetime.utcnow()
# #             }])
# #         })
        
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": True,
# #                 "data": {
# #                     "groupId": group_id,
# #                     "question": new_question
# #                 }
# #             }, default=str),
# #             headers={"Content-Type": "application/json"}
# #         )
        
# #     except Exception as e:
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": False,
# #                 "error": str(e)
# #             }),
# #             status=500,
# #             headers={"Content-Type": "application/json"}
# #         )
    
# # @https_fn.on_request()
# # def post_next_question(request: https_fn.Request) -> https_fn.Response:
# #     try:
# #         # Get group ID from request
# #         data = request.get_json()
# #         group_id = data.get('groupId')
        
# #         if not group_id:
# #             return https_fn.Response(
# #                 response=json.dumps({
# #                     "success": False,
# #                     "error": "Group ID is required"
# #                 }),
# #                 status=400,
# #                 headers={"Content-Type": "application/json"}
# #             )
        
# #         db = firestore.client()
# #         group_ref = db.collection('groups').document(group_id)
# #         group_doc = group_ref.get()
        
# #         if not group_doc.exists:
# #             return https_fn.Response(
# #                 response=json.dumps({
# #                     "success": False,
# #                     "error": "Group not found"
# #                 }),
# #                 status=404,
# #                 headers={"Content-Type": "application/json"}
# #             )
        
# #         group_data = group_doc.to_dict()
# #         next_questions = group_data.get('next_questions', [])
        
# #         # Check if there are any questions in the queue
# #         if not next_questions:
# #             return https_fn.Response(
# #                 response=json.dumps({
# #                     "success": False,
# #                     "error": "No questions in queue"
# #                 }),
# #                 status=404,
# #                 headers={"Content-Type": "application/json"}
# #             )
        
# #         # Get the first question
# #         next_question = next_questions[0]
# #         remaining_questions = next_questions[1:]
        
# #         # Create message data for the question
# #         message_data = {
# #             "_id": str(uuid.uuid4()),
# #             "text": next_question['text'],
# #             "user": {
# #                 "_id": "SYSTEM"  # or whatever ID you want to use for system messages
# #             },
# #             "createdAt": datetime.utcnow()
# #         }
        
# #         # Update the document in a transaction to ensure atomicity
# #         @firestore.transactional
# #         def update_in_transaction(transaction, group_ref):
# #             # Add to messages array and update next_questions array
# #             transaction.update(group_ref, {
# #                 'messages': firestore.ArrayUnion([message_data]),
# #                 'next_questions': remaining_questions
# #             })
        
# #         # Run the transaction
# #         transaction = db.transaction()
# #         update_in_transaction(transaction, group_ref)
        
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": True,
# #                 "data": {
# #                     "messageId": message_data["_id"],
# #                     "groupId": group_id,
# #                     "question": message_data["text"],
# #                     "remainingQuestions": len(remaining_questions)
# #                 }
# #             }, default=str),
# #             headers={"Content-Type": "application/json"}
# #         )
        
# #     except Exception as e:
# #         return https_fn.Response(
# #             response=json.dumps({
# #                 "success": False,
# #                 "error": str(e)
# #             }),
# #             status=500,
# #             headers={"Content-Type": "application/json"}
# #         )