from datetime import timedelta, datetime

from typing_extensions import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from ..database import SessionLocal
from ..models import Users
from passlib.context import CryptContext # to install this package, run pip install passlib
from starlette import status  # to install this package, run pip install starlette
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  #to install this package, run pip install fastapi[security]
from jose import jwt  # to install this package, run pip install python-jose[cryptography]
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

SECRET_KEY = "mysecretkeyreferwfg43t43t43gregrhg54g54g54g"
ALGORITHM = "HS256"  #read more types of algo##

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int,role: str , expires_delta: timedelta):
    to_encode = {"sub": username, "user_id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return {"username": username, "user_id": user_id, "role": user_role}


async def get_current_user_from_token(token: str):
    """Validate JWT token and return user info without database dependency."""
    try:
        if not token:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            return None
        return {"username": username, "user_id": user_id, "role": user_role}
    except jwt.JWTError:
        return None

user_dependency = Annotated[dict, Depends(get_current_user)]

templates = Jinja2Templates(directory="TodoApp/templates")

### Pages ###

@router.get("/login-page")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

### Endpoints ###


class CreateUserRequest(BaseModel):
    username: str = Field(min_length = 3, max_length = 50)
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str = Field(min_length=10, max_length=15)

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True,
        phone_number = create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()

    return create_user_model


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed to authenticate'
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))

    return Token(access_token=token, token_type="bearer")

#Assignment: Here is a opportunity to keep learning!

#1. Add a phone number field as required when we create a new user within our auth.py file.
#2. create a @put request in our users.py file that allows a user to update their phone number


@router.put('/update-phone-number/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(db:db_dependency, phone_number: str, user: user_dependency):
    user_info = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_info.phone_number = phone_number
    db.add(user_info)
    db.commit()


# @router.get("/auth/")
# async def get_user(db: db_dependency):
#     return {db.query(Users).all()}