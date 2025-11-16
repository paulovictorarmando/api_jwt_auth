from fastapi.testclient import TestClient
from main import app
from sqlmodel import SQLModel, create_engine, Session
import pytest
import os
import tempfile
from config.connection import get_session

# Use a file-based SQLite database for testing to ensure all connections share the same database
TEST_DB_FILE = tempfile.mktemp(suffix='.db')
TEST_ENGINE = create_engine(f"sqlite:///{TEST_DB_FILE}", connect_args={"check_same_thread": False})

# Cria o banco antes de tudo
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    from model.Usuario import Usuario
    SQLModel.metadata.create_all(TEST_ENGINE)
    yield
    SQLModel.metadata.drop_all(TEST_ENGINE)
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

# Sessão compartilhada
@pytest.fixture
def session_test():
    with Session(TEST_ENGINE) as session:
        yield session

# Client que usa override
@pytest.fixture
def client(session_test):
    def override_get_session():
        yield session_test
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
