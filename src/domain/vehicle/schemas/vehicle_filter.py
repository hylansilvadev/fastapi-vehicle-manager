from typing import Optional

from sqlmodel import SQLModel


class VehicleFilter(SQLModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[str] = None
    placa: Optional[str] = None
    cor: Optional[str] = None
    preco: Optional[str] = None
    proprietario: Optional[str] = None
    km: Optional[str] = None
    skip: Optional[int] = 0
    limit: Optional[int] = 100
    order_by: Optional[str] = 'created_at'
    order_dir: Optional[str] = 'desc'
