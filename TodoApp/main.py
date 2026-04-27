from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()


Base.metadata.create_all(bind = engine) # This line creates the database tables based on the models defined in the models.py file. The metadata of the Base class is used to create the tables, and the bind parameter is set to the engine created in the database.py file to specify the database connection.

app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static") # This line mounts the static files directory to serve static assets like CSS, JavaScript, and images. The StaticFiles class is used to specify the directory where the static files are located, and the name parameter is set to "static" to define the URL path for accessing these files.

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def read_healthy():
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
