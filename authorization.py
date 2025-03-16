from oso import Oso
from app.models import User
from app.database import get_db


oso = Oso()
oso.register_class(User)
oso.load_files(["C:/Webmavericks/Tasks/Task 4/FastApi/fastapi_app/app/policy.polar"])


# Check permissions
def check_permission(user: User, action: str, resource):
    print(f"Checking permission for User: {user}, Action: {action}, Resource: {resource}")
    if not isinstance(user, User):
        raise Exception("Invalid user object passed to authorization")

    if oso.is_allowed(user, action, resource):
        return True
    else:
        raise Exception("Permission denied")
