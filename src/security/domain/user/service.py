from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from src.core.database import get_session
from src.core.settings import settings
from src.security.domain.user import repository
from src.security.domain.user.model import User
from src.security.domain.user.schemas import user_schemas
from src.security.domain.user.schemas.user_schemas import TokenData
from src.security.services.auth_config import get_password_hash, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_user_by_email(session: Session, email: str) -> User | None:
    return repository.get_user_by_email(session, email)

def create_user(session: Session, user_in: user_schemas.UserCreate) -> User:
    db_user = repository.get_user_by_email(session, user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_password
    )
    # Copia outros atributos se existirem no UserCreate, como username se voltar a usar
    if hasattr(user_in, 'username') and user_in.username:
        new_user.username = user_in.username
    if hasattr(user_in, 'full_name') and user_in.full_name:
        new_user.full_name = user_in.full_name

    return repository.create_user(session, new_user)

def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = repository.get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = repository.get_user_by_email(session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not getattr(current_user, "is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
