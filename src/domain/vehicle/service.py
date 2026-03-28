from typing import List
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.core.exceptions import ConflictException, NotFoundException
from src.domain.vehicle.schemas import VehicleCreate, VehicleFilter, VehicleUpdate
from src.domain.vehicle.model import Vehicle
from src.domain.vehicle.repository import VehicleRepository


class VehicleService:
    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    def create_vehicle(self, data: VehicleCreate) -> Vehicle:
        vehicle = Vehicle.model_validate(data)
        try:
            return self.repository.create(vehicle)
        except IntegrityError as e:
            self.repository.session.rollback()
            raise ConflictException(
                message=f'Um veículo com a placa {data.placa} já está cadastrado.'
            )
        except Exception as e:
            if 'UniqueViolation' in str(e) or 'psycopg2.errors.UniqueViolation' in str(
                e.args
            ):
                self.repository.session.rollback()
                raise ConflictException(
                    message=f'Um veículo com a placa {data.placa} já está cadastrado.'
                )
            raise e

    def get_vehicle(self, vehicle_id: UUID) -> Vehicle:
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise NotFoundException(
                message=f'Veículo com id {vehicle_id} não encontrado.'
            )
        return vehicle

    def list_vehicles(self, filter_params: VehicleFilter) -> List[Vehicle]:
        return self.repository.get_all(filter_params)

    def update_vehicle(self, vehicle_id: UUID, data: VehicleUpdate) -> Vehicle:
        vehicle = self.get_vehicle(vehicle_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(vehicle, key, value)
        return self.repository.update(vehicle)

    def delete_vehicle(self, vehicle_id: UUID) -> None:
        vehicle = self.get_vehicle(vehicle_id)
        self.repository.delete(vehicle)
