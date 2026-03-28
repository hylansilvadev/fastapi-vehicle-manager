from typing import Optional

from sqlmodel import Field, SQLModel

from src.shared.model._base import _Base


class VehicleBase(SQLModel):
    marca: str = Field(index=True)
    modelo: str
    ano: str
    placa: str = Field(unique=True, index=True)
    cor: Optional[str] = None
    preco: Optional[str] = None
    proprietario: Optional[str] = None
    km: Optional[str] = None


class Vehicle(VehicleBase, _Base, table=True):
    __tablename__ = 'vehicle'
    ...
