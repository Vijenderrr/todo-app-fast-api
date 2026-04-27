from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from ..models import Todos
from ..database import SessionLocal
from starlette import status
from .auth import get_current_user, get_current_user_from_token
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="TodoApp/templates")

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)] # This line defines a dependency for the database session. It uses the Depends function to specify that the get_db function should be called to obtain a database session whenever this dependency is used in the endpoint functions. The Annotated type is used to indicate that the parameter is of type Session and that it depends on the get_db function.
user_dependency = Annotated[dict, Depends(get_current_user)] # This line defines a dependency for the current user. It uses the Depends function to specify that the get_current_user function should be called to obtain the current user's information whenever this dependency is used in the endpoint functions. The Annotated type is used to indicate that the parameter is of type dict and that it depends on the get_current_user function.

class TodoRequest(BaseModel):
    title: str = Field(min_length = 3)
    description: str = Field(min_length = 3, max_length = 100)
    priority: int = Field(gt = 0, lt = 6)
    completed: bool = Field(default=False)

def redirect_to_login():
    redirect_response =  RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie("access_token")
    return redirect_response


### Pages ###
@router.get("/todo-page", status_code=status.HTTP_200_OK)
async def render_todo_page(request: Request, db: db_dependency):
    try:
        token = request.cookies.get("access_token")
        user = await get_current_user_from_token(token)

        if user is None:
            return redirect_to_login()
        
        todos = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()

        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})
    
    except HTTPException:
        return redirect_to_login()


@router.get('/add-todo-page')
async def render_todo_page(request: Request, db: db_dependency):
    try:
        token = request.cookies.get("access_token")
        user = await get_current_user_from_token(token)

        if user is None:
            return redirect_to_login()
        
        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})
    
    except HTTPException:
        return redirect_to_login()

@router.get('/edit-todo-page/{todo_id}')
async def render_edit_todo_page(request: Request, db: db_dependency, todo_id: int = Path(gt=0)):
    try:
        token = request.cookies.get("access_token")
        user = await get_current_user_from_token(token)

        if user is None:
            return redirect_to_login()
        
        todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse("edit-todo.html", {"request": request, "user": user, "todo": todo_model})
    
    except HTTPException:
        return redirect_to_login()
    


### Endpoints ###

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency): # This line defines a GET endpoint at the root URL ("/") of the API. The function read_all is an asynchronous function that takes a database session as a parameter, which is obtained using the Depends dependency injection system to call the get_db function. The function will return all the todo items from the database when this endpoint is accessed.
    return db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)): # This line defines a GET endpoint at the URL "/todo/{todo_id}", where {todo_id} is a path parameter that represents the ID of a specific todo item. The function read_todo is an asynchronous function that takes a database session and the todo_id as parameters. It will return the specific todo item from the database that matches the provided ID when this endpoint is accessed.
    
    if user is None:
        raise HTTPException(status_code = 401, detail = "Unauthorized")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")


@router.post("/todo",status_code = status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code = 401, detail="Unauthorized")
    todo_model = Todos(**todo_request.dict(), owner_id = user.get("user_id"))

    db.add(todo_model)
    db.commit()



@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0), todo_request: TodoRequest = None):
    if user is None:
        raise HTTPException(status_code = 401, detail="Unauthorized")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()



@router.delete("/todo/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code = 401, detail="Unauthorized")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).delete()
    db.commit()