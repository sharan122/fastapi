# Define roles
actor_has_role(actor: User, "admin") if
    actor.role = "admin";

actor_has_role(actor: User, "user") if
    actor.role = "user";

# Admins can manage all users
allow(actor, "manage", "users") if
    actor_has_role(actor, "admin");

# Users can only update their own profiles
allow(actor, "update", user: User) if
    actor_has_role(actor, "user") and actor.id = user.id;
