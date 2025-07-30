from pydantic import BaseModel, Field
from typing import Optional

from pydantic import BaseModel, Field

class PersonaBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    apellido: str = Field(..., min_length=1)
    documento: str = Field(..., min_length=1)
    tipo_documento: int = Field(..., gt=0)

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(PersonaBase):
    pass

