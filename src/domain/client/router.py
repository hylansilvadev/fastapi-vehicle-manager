from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.core.database import get_session
from src.domain.client.schemas.register import ClientRegisterRequest, ClientRegisterResponse
from src.domain.client.service import ClientService

router = APIRouter(prefix="/clients", tags=["Clients"])


def get_client_service(session: Session = Depends(get_session)) -> ClientService:
    return ClientService(session)


@router.post(
    "/register",
    response_model=ClientRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo cliente",
    description="Cria registro de usuário de sistema, endereço e informações do cliente vinculados numa única transação atômica."
)
def register_client(
    payload: ClientRegisterRequest,
    service: ClientService = Depends(get_client_service),
):
    """
    Cadastra um cliente e seu respectivo usuário de acesso ao sistema juntamente com
    o seu endereço padrão. Não cria associação de veículos no primeiro momento.
    """
    return service.register_client(payload)
