from sqlmodel import Field

from src.shared.model._base import _Base


class Address(_Base, table=True):
    __tablename__ = "addresses"

    street: str = Field(nullable=False)
    number: str = Field(nullable=True)
    has_number: bool = Field(default=True, nullable=False)
    complement: str = Field(nullable=True)
    city: str = Field(nullable=False)
    state: str = Field(nullable=False)
    zip_code: str = Field(nullable=False)

    def __str__(self) -> str:
        parts = [self.street]
        
        if self.has_number and self.number:
            parts.append(self.number)
        
        if self.complement:
            parts.append(self.complement)
        
        parts.extend([self.city, self.state, self.zip_code])
        
        return ", ".join(parts)