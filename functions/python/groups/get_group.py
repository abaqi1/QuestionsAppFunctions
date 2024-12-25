from firebase_functions import https_fn
import json
from firebase_admin import firestore
from python.utils.firebase_init import db

# Get a specific group by ID
@https_fn.on_request()
def get_group(request: https_fn.Request) -> https_fn.Response:
    try:
        group_id = request.args.get('id')
        if not group_id:
            return https_fn.Response(
                response=json.dumps({
                    "success": False,
                    "error": "Group ID is required"
                }),
                status=400,
                headers={"Content-Type": "application/json"}
            )
        
        doc = db.collection('groups').document(group_id).get()
        
        if not doc.exists:
            return https_fn.Response(
                response=json.dumps({
                    "success": False,
                    "error": "Group not found"
                }),
                status=404,
                headers={"Content-Type": "application/json"}
            )
        
        group_data = doc.to_dict()
        group_data['id'] = doc.id
        
        # Get users in this group
        users_ref = db.collection('users').where('groupId', '==', group_id).stream()
        users = []
        for user_doc in users_ref:
            user_data = user_doc.to_dict()
            user_data['id'] = user_doc.id
            users.append(user_data)
        
        group_data['users'] = users
        
        return https_fn.Response(
            response=json.dumps({
                "success": True,
                "data": group_data
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