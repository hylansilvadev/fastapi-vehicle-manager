from typing import Optional

from sqlmodel import Session, select

from src.domain.client.model import Client
from src.security.domain.user.model import User
from src.shared.model.address import Address


class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def create_full_client(self, user: User, address: Address, client: Client) -> Client:
        try:
            self.session.add(user)
            self.session.add(address)
            self.session.flush()

            client.user_id = user.id
            client.address_id = address.id
            
            self.session.add(client)
            self.session.commit()
            
            self.session.refresh(client)
            return client
        except Exception as e:
            self.session.rollback()
            raise e

