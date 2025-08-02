from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db, Base
from services.auth_serivce import get_current_user
from fastapi import HTTPException, status, Request
import pytest

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def override_get_current_user(request: Request):
    if "authorization" not in request.headers:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return {"user_id": 1, "username": "testuser", "email": "test@example.com"}

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def setup_database():
    Base.metadata.create_all(bind=engine)

def teardown_database():
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_organization():
    return {
        "organization_name": "Test Organization"
    }


@pytest.fixture
def test_channel(test_organization):
    return {
        "channel_name": "Test Channel",
        "organization_id": 1
    }


@pytest.fixture
def test_topic(test_channel):
    return {
        "topic_name": "Test Topic",
        "channel_id": 1,
        "organization_id": 1
    }

@pytest.fixture
def headers():
    return {"Authorization": "Bearer test-token"}