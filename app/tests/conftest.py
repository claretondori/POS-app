import os
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


os.environ["DATABASE_URL"] = "sqlite://"

from app.database import Base, get_db
from app.dependencies import get_current_user
from app.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def _override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def _override_get_current_user():
    """Stand-in for a logged-in user.

    There's no login endpoint wired up yet, so protected routers (currently
    just /products) are exercised by overriding this dependency directly
    instead of pushing a real JWT through the auth flow.
    """
    return SimpleNamespace(user_id=1, username="clare_test", is_active=True)


@pytest.fixture
def client():
    """TestClient backed by a fresh, isolated SQLite database for each test.

    No auth override here - this is also what we use to prove protected
    endpoints correctly reject unauthenticated requests.
    """
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = _override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def authed_client(client):
    """Same isolated database as `client`, acting as an authenticated user."""
    app.dependency_overrides[get_current_user] = _override_get_current_user
    yield client

