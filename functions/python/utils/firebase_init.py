import firebase_admin
from firebase_admin import firestore, initialize_app, credentials
import os
from config.firebase_config import FIREBASE_CONFIG


# Environment variable to control emulator usage
USE_EMULATOR = os.getenv('USE_EMULATOR', 'false').lower() == 'true'
config = FIREBASE_CONFIG['emulator'] if USE_EMULATOR else FIREBASE_CONFIG['cloud']

# Initialize Firebase only once
if USE_EMULATOR:
    os.environ["FIRESTORE_EMULATOR_HOST"] = config['firestore_host']
    os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = config['auth_host']
    firebase_admin.initialize_app(options={'projectId': config['projectId']})
else:
    cred = credentials.Certificate(config['credentials_path'])
    initialize_app(cred)

# Create a db client that can be imported by other modules
db = firestore.client()