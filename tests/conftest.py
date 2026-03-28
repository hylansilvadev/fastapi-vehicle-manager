import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from src.core.database import get_session

# Banco de dados em memória para testes
sqlite_url = 'sqlite://'
engine = create_engine(
    sqlite_url,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)


@pytest.fixture(name='session')
def session_fixture():
    # Cria as tabelas no banco em memória
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Após o teste, limpa as tabelas
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name='client')
def client_fixture(session: Session):
    # Sobrescreve a dependência de sessão do banco
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
