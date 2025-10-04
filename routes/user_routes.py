from fastapi import APIRouter, HTTPException
from typing import List
from schemas.user import User, UserCreate, UserUpdate
from services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate):
    """
    Create a new user.
    Returns the created user record.
    """
    return user_service.create_user(user)


@router.get("/", response_model=List[User])
def list_users():
    """
    Retrieve all registered users.
    """
    return user_service.get_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    """
    Retrieve a user by ID.
    Raises 404 if the user does not exist.
    """
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """
    Update user details (e.g., name or email).
    Raises 404 if the user does not exist.
    """
    updated_user = user_service.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.put("/{user_id}/deactivate")
def deactivate_user(user_id: int):
    """
    Deactivate a user account.
    Returns a success message if successful.
    """
    success = user_service.deactivate_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deactivated successfully"}
