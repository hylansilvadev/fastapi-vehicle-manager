from typing import Optional

from sqlmodel import Field

from src.shared.model._base import _Base


class User(_Base, table=True):
    __tablename__ = "usuarios"
    email: Optional[str] = Field(default=None, unique=True, index=True)
    is_email_verified: bool = Field(default=False)
    hashed_password: str
    is_active: bool = Field(default=True)
