from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_autheticated(test_todo):
    response = client.get("/admin/todo")
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



def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verify the item was actually deleted from the database
    db = TestingSessionLocal()
    todo_in_db = db.query(Todos).filter(Todos.id == 1).first()
    assert todo_in_db is None


def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with id 999 not found"}