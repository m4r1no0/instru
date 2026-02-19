from pydantic import BaseModel, Field
from typing import Optional


# =====================================
# BASE
# =====================================
class SupervisorBase(BaseModel):
    nombre: Optional[str] = Field(default=None, max_length=30)


# =====================================
# CREAR
# =====================================
class SupervisorCreate(SupervisorBase):
    pass


# =====================================
# ACTUALIZAR
# =====================================
class SupervisorUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, max_length=30)


# =====================================
# RESPUESTA
# =====================================
class SupervisorOut(SupervisorBase):
    id_supervisor: int

    class Config:
        from_attributes = True
