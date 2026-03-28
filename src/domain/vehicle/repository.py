from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from src.domain.vehicle.schemas import VehicleFilter
from src.domain.vehicle.model import Vehicle


class VehicleRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, vehicle: Vehicle) -> Vehicle:
        self.session.add(vehicle)
        self.session.commit()
        self.session.refresh(vehicle)
        return vehicle

    def get_by_id(self, vehicle_id: UUID) -> Optional[Vehicle]:
        return self.session.get(Vehicle, vehicle_id)

    def get_all(self, filter_params: VehicleFilter) -> List[Vehicle]:
        query = select(Vehicle)

        # Mapeia os campos que requerem busca parcial (LIKE)
        text_fields = ['marca', 'modelo', 'placa', 'cor', 'proprietario']
        for field in text_fields:
            value = getattr(filter_params, field)
            if value:
                column = getattr(Vehicle, field)
                query = query.where(column.ilike(f'%{value}%'))

        # Mapeia os campos de busca exata
        exact_fields = ['ano', 'preco', 'km']
        for field in exact_fields:
            value = getattr(filter_params, field)
            if value is not None:
                column = getattr(Vehicle, field)
                query = query.where(column == value)

        sort_col = getattr(Vehicle, filter_params.order_by, Vehicle.created_at)
        if filter_params.order_dir == 'desc':
            query = query.order_by(sort_col.desc())
        else:
            query = query.order_by(sort_col.asc())

        return list(
            self.session.exec(
                query.offset(filter_params.skip).limit(filter_params.limit)
            ).all()
        )

    def update(self, vehicle: Vehicle) -> Vehicle:
        self.session.add(vehicle)
        self.session.commit()
        self.session.refresh(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self.session.delete(vehicle)
        self.session.commit()
