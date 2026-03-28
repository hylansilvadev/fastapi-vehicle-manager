from typing import Optional

from sqlmodel import SQLModel


class VehicleUpdate(SQLModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[str] = None
    placa: Optional[str] = None
    cor: Optional[str] = None
    preco: Optional[str] = None
    proprietario: Optional[str] = None
    km: Optional[str] = None
