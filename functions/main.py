from firebase_functions import https_fn, options
from python.groups.get_groups import get_groups
from python.users.get_users import get_users
from python.groups.get_group import get_group
from python.messages.add_message import add_message
from python.groups.generate_group_question import generate_group_question
from python.groups.generate_test_question import generate_test_question
from python.messages.post_next_question import post_next_question
    
# Export all functions
exports = {
    'get_groups': get_groups,
    'get_users': get_users,
    'get_group': get_group,
    'add_message': add_message,
    'generate_group_question': generate_group_question,
    'generate_test_question': generate_test_question,
    'post_next_question': post_next_question
}