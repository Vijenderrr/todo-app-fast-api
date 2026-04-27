from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Path
from ..models import Todos, Users
from ..database import SessionLocal
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext # to install this package, run pip install passlib


router = APIRouter(
    prefix = '/users',
    tags = ['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)] # This line defines a dependency for the database session. It uses the Depends function to specify that the get_db function should be called to obtain a database session whenever this dependency is used in the endpoint functions. The Annotated type is used to indicate that the parameter is of type Session and that it depends on the get_db function.
user_dependency = Annotated[dict, Depends(get_current_user)] # This line defines a dependency for the current user. It uses the Depends function to specify that the get_current_user function should be called to obtain the current user's information whenever this dependency is used in the endpoint functions. The Annotated type is used to indicate that the parameter is of type dict and that it depends on the get_current_user function.
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

## Assignement: Here is a opportunity to keep learning!

# 1. Create a new route called Users.
# 2. Then create 2 new API Endpoints
#   a. get_user: this endpoint should return all the information about the user that is currently logged in.
#   b. change_password: this endpoint should allow a user to change their current password. 

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user: user_dependency):
    user_info = db.query(Users).filter(Users.id == user.get('user_id')).first()
    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info


@router.put('/change-password/{new_password}', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db: db_dependency, user: user_dependency, new_password: str):
    user_info = db.query(Users).filter(Users.id == user.get('user_id')).first()

    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    

    user_info.hashed_password = bcrypt_context.hash(new_password)
    db.add(user_info)
    db.commit()
