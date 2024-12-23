from firebase_functions import https_fn, options
import firebase_admin
from firebase_admin import firestore, initialize_app
import json
import os
from config.firebase_config import FIREBASE_CONFIG
from db_accessor import (
    get_groups,
    get_users,
    get_group
)

# Set region for functions
options.set_global_options(region="us-central1")

# Re-export all functions
get_groups_endpoint = get_groups
get_users_endpoint = get_users
get_group_endpoint = get_group