"""
Integration tests for the Todos API using FastAPI's TestClient.

These tests run against an isolated, shared in-memory SQLite database and
leverage FastAPI dependency overrides to inject a test Session and a
deterministic authenticated user (role=admin). This ensures tests are
repeatable and do not depend on any developer machine state.
"""

from TodoApp.routers.auth import get_current_user
from TodoApp.test.utils import (
    override_get_current_user,
    override_get_db,
    client,
    TestingSessionLocal,
    test_todo,  # pytest fixture imported from utils so tests can use it
)
from ..main import app
from TodoApp.routers.todos import get_db
from TodoApp.routers import admin as admin_router
from starlette import status 
from ..models import Todos



# Wire dependency overrides so all endpoints use the test session and
# the test user. Note: override both references to get_db to match by
# callable identity across routers.
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[admin_router.get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    """Admin can list all todos and see the seeded row."""
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    items = response.json()
    assert isinstance(items, list)
    assert len(items) == 1
    item = items[0]
    assert item['title'] == 'Learn FastAPI'
    assert item['description'] == 'Learn how to use FastAPI for building APIs'
    assert item['priority'] == 1
    assert item['owner_id'] == 1
    assert item['completed'] is False



def test_read_one_authenticated(test_todo):
    """Admin can retrieve a specific todo by id."""
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'title': 'Learn FastAPI',
        'description': 'Learn how to use FastAPI for building APIs',
        'priority': 1,
        'owner_id': 1,
        'completed': False
    }


def test_read_one_authenticated_not_found():
    """Retrieving a non-existent todo returns 404 with a helpful message."""
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with id 999 not found"}


def test_create_todo(test_todo):
    """Admin can create a new todo and it persists to the DB."""
    request_data ={
        "title": "Learn SQLAlchemy",
        "description": "Learn how to use SQLAlchemy for database interactions",
        "priority": 2,
        "completed": False
    }
    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model is not None
    assert model.title == "Learn SQLAlchemy"
    assert model.description == "Learn how to use SQLAlchemy for database interactions"
    assert model.priority == 2
    assert model.completed is False
    assert model.owner_id == 1



def test_update_todo(test_todo):
    """Admin can update an existing todo and changes are persisted."""
    request_data ={
        "title": "Learn FastAPI - Updated",
        "description": "Learn how to use FastAPI for building APIs - Updated",
        "priority": 3,
        "completed": True
    }
    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is not None
    assert model.title == "Learn FastAPI - Updated"
    assert model.description == "Learn how to use FastAPI for building APIs - Updated"
    assert model.priority == 3
    assert model.completed is True


def test_delete_todo(test_todo):
    """Admin can delete an existing todo and it is removed from the DB."""
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    """Deleting a non-existent todo returns 404 with a helpful message."""
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with id 999 not found"}