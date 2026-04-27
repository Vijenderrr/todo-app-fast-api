from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Path
from ..models import Todos
from ..database import SessionLocal
from starlette import status
from .auth import get_current_user

router = APIRouter(
    prefix = '/admin',
    tags = ['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)] # This line defines a dependency for the database session. It uses the Depends function to specify that the get_db function should be called to obtain a database session whenever this dependency is used in the endpoint functions. The Annotated type is used to indicate that the parameter is of type Session and that it depends on the get_db function.
user_dependency = Annotated[dict, Depends(get_current_user)] # This line defines a dependency for the current user. It uses the Depends function to specify that the get_current_user function should be called to obtain the current user's information whenever this dependency is used in the endpoint functions. The Annotated type is used to indicate that the parameter is of type dict and that it depends on the get_current_user function.


@router.get("/todo", status_code = status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code = 401, detail='Authentication failed')
    return db.query(Todos).all()

@router.delete("/todo/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code = 401, detail='Authentication failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()