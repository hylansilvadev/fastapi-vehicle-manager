from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from src.core.database import get_session
from src.domain.vehicle.schemas import VehicleCreate, VehicleFilter, VehicleUpdate
from src.domain.vehicle.model import Vehicle
from src.domain.vehicle.repository import VehicleRepository
from src.domain.vehicle.service import VehicleService

router = APIRouter(prefix='/vehicles', tags=['Vehicles'])


def get_vehicle_service(session: Session = Depends(get_session)) -> VehicleService:
    repository = VehicleRepository(session)
    return VehicleService(repository)


@router.post('/', response_model=Vehicle, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    data: VehicleCreate, service: VehicleService = Depends(get_vehicle_service)
):
    """
    Cria um novo veículo.
    """
    return service.create_vehicle(data)


@router.get('/', response_model=List[Vehicle])
def list_vehicles(
    filter_params: VehicleFilter = Depends(),
    service: VehicleService = Depends(get_vehicle_service),
):
    """
    Lista os veículos mapeando os parâmetros da URL (Query String) para o padrão de objeto de Filtros.
    """
    return service.list_vehicles(filter_params)


@router.get('/{vehicle_id}', response_model=Vehicle)
def get_vehicle(
    vehicle_id: UUID, service: VehicleService = Depends(get_vehicle_service)
):
    """
    Retorna um veículo específico pelo ID.
    """
    return service.get_vehicle(vehicle_id)


@router.patch('/{vehicle_id}', response_model=Vehicle)
def update_vehicle(
    vehicle_id: UUID,
    data: VehicleUpdate,
    service: VehicleService = Depends(get_vehicle_service),
):
    """
    Atualiza parcialmente os dados do veículo.
    """
    return service.update_vehicle(vehicle_id, data)


@router.delete('/{vehicle_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: UUID, service: VehicleService = Depends(get_vehicle_service)
):
    """
    Remove um veículo permanentemente.
    """
    service.delete_vehicle(vehicle_id)
