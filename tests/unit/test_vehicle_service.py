import uuid
from unittest.mock import MagicMock

import pytest

from src.core.exceptions import ConflictException, NotFoundException
from src.domain.vehicle.schemas import VehicleCreate, VehicleUpdate
from src.domain.vehicle.model import Vehicle
from src.domain.vehicle.service import VehicleService


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def vehicle_service(mock_repo):
    # Injeta um mock do repositório no service
    return VehicleService(mock_repo)


def test_create_vehicle_success(vehicle_service, mock_repo):
    """
    Testa a criação de um veículo com sucesso.
    """
    # Dado (Given)
    dto = VehicleCreate(
        marca='Toyota',
        modelo='Corolla',
        placa='ABC-1234',
        ano='2022',
        cor='Prata',
        preco='120000.0',
        proprietario='João Silva',
        km='15000',
    )

    mock_vehicle = Vehicle(**dto.model_dump())
    mock_vehicle.id = uuid.uuid4()
    mock_repo.create.return_value = mock_vehicle

    # Quando (When)
    result = vehicle_service.create_vehicle(dto)

    # Então (Then)
    assert result.placa == 'ABC-1234'
    assert result.id is not None
    mock_repo.create.assert_called_once()


def test_create_vehicle_duplicate_placa(vehicle_service, mock_repo):
    """
    Testa a criação de um veículo com uma placa já existente, simulando um erro de unicidade.
    """
    # Dado (Given)
    dto = VehicleCreate(
        marca='Toyota',
        modelo='Corolla',
        placa='ABC-1234',
        ano='2022',
        cor='Prata',
        preco='120000.0',
        proprietario='João Silva',
        km='15000',
    )

    # Simula erro de Unicidade
    mock_repo.create.side_effect = Exception('psycopg2.errors.UniqueViolation')
    mock_repo.session.rollback = MagicMock()

    # Quando (When) / Então (Then)
    with pytest.raises(ConflictException) as exc_info:
        vehicle_service.create_vehicle(dto)

    assert 'está cadastrado' in str(exc_info.value) or exc_info.value.status_code == 409


def test_get_by_id_success(vehicle_service, mock_repo):
    """
    Testa a obtenção de um veículo por ID com sucesso.
    """
    # Dado (Given)
    v_id = uuid.uuid4()
    mock_v = Vehicle(id=v_id, marca='Ford', modelo='Ka', placa='XYZ-1234', ano='2020')
    mock_repo.get_by_id.return_value = mock_v

    # Quando (When)
    result = vehicle_service.get_vehicle(v_id)

    # Então (Then)
    assert result.id == v_id
    mock_repo.get_by_id.assert_called_once_with(v_id)


def test_get_by_id_not_found(vehicle_service, mock_repo):
    """
    Testa a obtenção de um veículo por ID que não existe.
    """
    # Dado (Given)
    v_id = uuid.uuid4()
    mock_repo.get_by_id.return_value = None

    # Quando (When) / Então (Then)
    with pytest.raises(NotFoundException):
        vehicle_service.get_vehicle(v_id)


def test_update_vehicle_success(vehicle_service, mock_repo):
    """
    Testa a atualização de um veículo com sucesso.
    """
    # Dado (Given)
    v_id = uuid.uuid4()
    mock_v = Vehicle(
        id=v_id,
        marca='Ford',
        modelo='Ka',
        placa='XYZ-1234',
        ano='2020',
        cor='Branco',
        preco='30000.0',
    )
    mock_repo.get_by_id.return_value = mock_v

    update_dto = VehicleUpdate(cor='Preto', preco='35000.0')
    updated_v = Vehicle(
        id=v_id,
        marca='Ford',
        modelo='Ka',
        placa='XYZ-1234',
        ano='2020',
        cor='Preto',
        preco='35000.0',
    )
    mock_repo.update.return_value = updated_v

    # Quando (When)
    result = vehicle_service.update_vehicle(v_id, update_dto)

    # Então (Then)
    assert result.cor == 'Preto'
    assert result.preco == '35000.0'
    mock_repo.update.assert_called_once()


def test_delete_vehicle_success(vehicle_service, mock_repo):
    """
    Testa a exclusão de um veículo com sucesso.
    """
    # Dado (Given)
    v_id = uuid.uuid4()
    mock_v = Vehicle(id=v_id, marca='Ford', modelo='Ka', placa='XYZ-1234', ano='2020')
    mock_repo.get_by_id.return_value = mock_v

    # Quando (When)
    result = vehicle_service.delete_vehicle(v_id)

    # Então (Then)
    assert result is None
    mock_repo.delete.assert_called_once_with(mock_v)


def test_create_vehicle_generic_exception(vehicle_service, mock_repo):
    """
    Testa se uma exceção genérica é propagada.
    """
    # Dado (Given)
    dto = VehicleCreate(marca='T', modelo='C', placa='XXX', ano='2022')
    mock_repo.create.side_effect = Exception('Some random error')

    # Quando (When) / Então (Then)
    with pytest.raises(Exception, match='Some random error'):
        vehicle_service.create_vehicle(dto)
