# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, options
import firebase_admin
from firebase_admin import firestore, initialize_app
import json
import os
from config.firebase_config import FIREBASE_CONFIG

# Environment variable to control emulator usage
USE_EMULATOR = os.getenv('USE_EMULATOR', 'true').lower() == 'true'

config = FIREBASE_CONFIG['emulator'] if USE_EMULATOR else FIREBASE_CONFIG['cloud']

if USE_EMULATOR:
    os.environ["FIRESTORE_EMULATOR_HOST"] = config['firestore_host']
    os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = config['auth_host']
    firebase_admin.initialize_app(options={'projectId': config['projectId']})
else:
    # cred = credentials.Certificate(config['credentials_path'])
    # firebase_admin.initialize_app(cred, {'projectId': config['projectId']})
    initialize_app()

# Set region for functions
options.set_global_options(region="us-central1")

@https_fn.on_request()
def get_groups(request: https_fn.Request) -> https_fn.Response:
    try:
        db = firestore.client()
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

@https_fn.on_request()
def test_emulator(request: https_fn.Request) -> https_fn.Response:
    try:
        db = firestore.client()
        # Try to write to emulator
        test_ref = db.collection('test').document('emulator-test')
        test_ref.set({
            'timestamp': firestore.SERVER_TIMESTAMP,
            'message': 'Testing emulator connection'
        })
        
        return https_fn.Response(
            response=json.dumps({
                "success": True,
                "message": "Successfully connected to Firestore emulator",
                "emulator_host": os.getenv("FIRESTORE_EMULATOR_HOST"),
                "auth_emulator": os.getenv("FIREBASE_AUTH_EMULATOR_HOST")
            }),
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return https_fn.Response(
            response=json.dumps({
                "success": False,
                "error": str(e),
                "emulator_host": os.getenv("FIRESTORE_EMULATOR_HOST")
            }),
            status=500,
            headers={"Content-Type": "application/json"}
        )

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
        
        db = firestore.client()
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