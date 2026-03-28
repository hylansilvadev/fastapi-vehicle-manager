from collections.abc import Generator

from sqlmodel import Session, create_engine

from .settings import settings

# Engine configurada sem a criação de tabelas automáticas
# Como o projeto utiliza Alembic para as migrações, não faremos SQLModel.metadata.create_all(engine)
engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
