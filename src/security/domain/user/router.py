from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.core.database import get_session
from src.core.settings import settings
from src.security.domain.user import service
from src.security.domain.user.model import User
from src.security.domain.user.schemas import user_schemas
from src.security.services.auth_config import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=user_schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
):
    user = service.authenticate_user(session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=user_schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: user_schemas.UserCreate,
    session: Session = Depends(get_session)
):
    return service.create_user(session, user_in)

@router.get("/users/me/", response_model=user_schemas.UserRead)
async def read_users_me(
    current_user: Annotated[User, Depends(service.get_current_active_user)],
):
    return current_user
