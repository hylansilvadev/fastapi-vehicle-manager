from fastapi import HTTPException, status
from sqlmodel import Session

from src.domain.client.model import Client
from src.domain.client.repository import ClientRepository
from src.domain.client.schemas.register import (
    ClientRegisterRequest,
    ClientRegisterResponse,
    AddressResponse,
    UserResponse
)
from src.security.domain.user.model import User
from src.security.services.auth_config import get_password_hash
from src.shared.model.address import Address


class ClientService:
    def __init__(self, session: Session):
        self.repository = ClientRepository(session)

    def register_client(self, request_data: ClientRegisterRequest) -> ClientRegisterResponse:
        # 1. Verificar se o e-mail já existe
        existing_user = self.repository.get_user_by_email(request_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado."
            )

        # 2. Criar registro em usuarios
        hashed_pw = get_password_hash(request_data.password)
        user = User(
            email=request_data.email,
            hashed_password=hashed_pw,
            is_active=True,
            is_email_verified=False
        )

        # 3. Criar registro em addresses
        address = Address(**request_data.address.model_dump())

        # 4. Preparar o cliente (links serão feitos no repository)
        client = Client(
            full_name=request_data.full_name,
            vehicle_id=None
        )

        # Usar unidade de trabalho do repositório para atomizar tudo
        try:
            created_client = self.repository.create_full_client(user, address, client)
        except Exception as e:
            # Em caso de falha de banco de dados genérica
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao criar cliente. Falha na transação."
            ) from e

        # 5. Retornar dados (omitindo senhas etc.)
        return ClientRegisterResponse(
            id=created_client.id,
            full_name=created_client.full_name,
            vehicle_id=created_client.vehicle_id,
            user=UserResponse(
                id=user.id,
                email=user.email,
                is_active=user.is_active,
                is_email_verified=user.is_email_verified
            ),
            address=AddressResponse(
                id=address.id,
                street=address.street,
                number=address.number,
                has_number=address.has_number,
                complement=address.complement,
                city=address.city,
                state=address.state,
                zip_code=address.zip_code
            )
        )
