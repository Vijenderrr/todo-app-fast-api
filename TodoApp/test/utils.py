
from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker

from TodoApp.database import Base
from sqlalchemy import create_engine


from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todos

# Use a single in-memory SQLite database for the entire test run.
# StaticPool guarantees the same connection is reused across threads,
# which is necessary because the ASGI app runs in a different thread.
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # allow cross-thread access for tests
    poolclass=StaticPool,                        # reuse the same in-memory DB connection
)


# Dedicated session factory for tests; disable expiration so assertions can
# read attributes after commit without reloading.
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

# Ensure a clean schema before tests run against the shared in-memory DB.
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Yield a scoped test session wired to the in-memory database."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    """Return a deterministic authenticated user with admin privileges."""
    return {"username": "admin", "user_id": 1, "user_role": "admin"}



client = TestClient(app)

@pytest.fixture
def test_todo():
    """Seed a single Todo row and clean up after the test."""
    todo = Todos(
        title= "Learn FastAPI",
        description= "Learn how to use FastAPI for building APIs",
        priority= 1,
        completed= False,
        owner_id= 1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()
