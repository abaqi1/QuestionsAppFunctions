from firebase_functions import https_fn
import json
import os
from firebase_admin import firestore
from python.utils.firebase_init import db, USE_EMULATOR

@https_fn.on_request()
def get_groups(request: https_fn.Request) -> https_fn.Response:
    try:
        if USE_EMULATOR:
            print("Using Firestore emulator at:", os.getenv("FIRESTORE_EMULATOR_HOST"))
        else:
            print("Using Cloud Firestore")
        
        groups_ref = db.collection('groups')
        docs = groups_ref.stream()
        
        groups = []
        for doc in docs:
            group_data = doc.to_dict()
            group_data['id'] = doc.id
            groups.append(group_data)
        
        return https_fn.Response(
            response=json.dumps({
                "success": True,
                "data": groups,
                "count": len(groups),
                "mode": "emulator" if USE_EMULATOR else "cloud",
                "emulator_host": os.getenv("FIRESTORE_EMULATOR_HOST") if USE_EMULATOR else None
            }, default=str),
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return https_fn.Response(
            response=json.dumps({
                "success": False,
                "error": str(e),
                "mode": "emulator" if USE_EMULATOR else "cloud"
            }),
            status=500,
            headers={"Content-Type": "application/json"}
        )