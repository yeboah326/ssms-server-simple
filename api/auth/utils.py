from typing import List
from api.auth.models import SchoolUser, SuperUser


def current_user_type(public_id: str, user_types: List[str]):
    user_status = {
        "super_user": SuperUser.user_is_super_user(public_id),
        "admin": SchoolUser.user_is_admin(public_id),
        "auditor": SchoolUser.user_is_auditor(public_id),
        "teacher": SchoolUser.user_is_teacher(public_id),
        "owner": SchoolUser.user_is_owner(public_id),
    }

    # False is used as the initial state because it is the identity OR operation
    state = False

    # Compare to the desired user statuses
    for user_type in user_types:
        state = state or user_status[user_type]

    return state
