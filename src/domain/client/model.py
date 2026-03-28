from uuid import UUID
from sqlmodel import Field

from src.shared.model._base import _Base


class Client(_Base, table=True):
    __tablename__ = "clients"

    full_name: str = Field(nullable=False)
    user_id: UUID = Field(foreign_key="usuarios.id", nullable=False)
    vehicle_id: UUID | None = Field(foreign_key="vehicle.id", nullable=True)
    address_id: UUID = Field(foreign_key="addresses.id", nullable=False)