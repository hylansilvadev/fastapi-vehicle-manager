from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class AddressCreate(BaseModel):
    street: str
    number: str
    has_number: bool
    complement: Optional[str] = None
    city: str
    state: str
    zip_code: str


class ClientRegisterRequest(BaseModel):
    # Auth
    email: EmailStr
    password: str = Field(min_length=6)

    # Cliente
    full_name: str

    # Endereço
    address: AddressCreate


class AddressResponse(BaseModel):
    id: UUID
    street: str
    number: Optional[str] = None
    has_number: bool
    complement: Optional[str] = None
    city: str
    state: str
    zip_code: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    is_active: bool
    is_email_verified: bool


class ClientRegisterResponse(BaseModel):
    id: UUID
    full_name: str
    vehicle_id: Optional[UUID] = None
    user: UserResponse
    address: AddressResponse
