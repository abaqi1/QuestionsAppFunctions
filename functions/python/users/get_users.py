from firebase_functions import https_fn
import json
import os
from firebase_admin import firestore
from python.utils.firebase_init import db
@https_fn.on_request()
def get_users(request: https_fn.Request) -> https_fn.Response:
    try:
        print("Connecting to Firestore emulator at:", os.getenv("FIRESTORE_EMULATOR_HOST"))
        group_id = request.args.get('groupId')
        limit = int(request.args.get('limit', '10'))
        
        db = firestore.client()
        users_ref = db.collection('users')
        
        if group_id:
            users_ref = users_ref.where('groupId', '==', group_id)
        
        docs = users_ref.limit(limit).stream()
        
        users = []
        for doc in docs:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            users.append(user_data)
        
        return https_fn.Response(
            response=json.dumps({
                "success": True,
                "data": users,
                "count": len(users),
                "filters": {
                    "groupId": group_id,
                    "limit": limit
                },
                "emulator": os.getenv("FIRESTORE_EMULATOR_HOST")
            }),
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return https_fn.Response(
            response=json.dumps({
                "success": False,
                "error": str(e),
                "emulator": os.getenv("FIRESTORE_EMULATOR_HOST")
            }),
            status=500,
            headers={"Content-Type": "application/json"}
        )