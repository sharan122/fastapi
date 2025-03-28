from oso import Oso
from models import User
from database import get_db


oso = Oso()
oso.register_class(User)
oso.load_files(["policy.polar"])


# Check permissions
def check_permission(user: User, action: str, resource):
    print(f"Checking permission for User: {user}, Action: {action}, Resource: {resource}")
    if not isinstance(user, User):
        raise Exception("Invalid user object passed to authorization")

    if oso.is_allowed(user, action, resource):
        return True
    else:
        raise Exception("Permission denied")
