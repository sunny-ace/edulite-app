from schemas.user import User, UserCreate, UserUpdate

users = []
user_id_counter = 1

def create_user(user: UserCreate) -> User:
    global user_id_counter
    new_user = User(id=user_id_counter, **user.dict())
    users.append(new_user)
    user_id_counter += 1
    return new_user

def get_users() -> list[User]:
    return users

def get_user(user_id: int) -> User | None:
    return next((u for u in users if u.id == user_id), None)

def update_user(user_id: int, user_update: UserUpdate) -> User | None:
    user = get_user(user_id)
    if user:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        return user
    return None

def deactivate_user(user_id: int) -> bool:
    user = get_user(user_id)
    if user:
        user.is_active = False
        return True
    return False
