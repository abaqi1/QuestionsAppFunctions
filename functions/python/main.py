from firebase_functions import https_fn, options
import firebase_admin
from firebase_admin import firestore, initialize_app
import json
import os
from config.firebase_config import FIREBASE_CONFIG
from db_accessor import (
    get_groups,
    get_users,
    get_group,
    add_message,
    generate_group_question,
    post_next_question,
    generate_test_question
)

# Set region for functions
options.set_global_options(region="us-central1")

# Re-export all functions
get_groups_endpoint = get_groups
get_users_endpoint = get_users
get_group_endpoint = get_group
add_message_endpoint = add_message
generate_group_question_endpoint = generate_group_question
post_next_question_endpoint = post_next_question
get_test_question_endpoint = generate_test_question