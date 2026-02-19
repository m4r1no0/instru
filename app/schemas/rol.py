from pydantic import BaseModel, Field, field_validator
from typing import Optional


# =====================================
# BASE
# =====================================
class RolBase(BaseModel):
    nombre: Optional[str] = Field(default=None, max_length=30)
    estado: int

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v):
        if v not in (0, 1):
            raise ValueError("El estado solo puede ser 0 (inactivo) o 1 (activo)")
        return v


# =====================================
# CREAR
# =====================================
class RolCreate(RolBase):
    pass


# =====================================
# ACTUALIZAR
# =====================================
class RolUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, max_length=30)
    estado: Optional[int] = None

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v):
        if v is not None and v not in (0, 1):
            raise ValueError("El estado solo puede ser 0 o 1")
        return v


# =====================================
# RESPUESTA
# =====================================
class RolOut(RolBase):
    id_rol: int

    class Config:
        from_attributes = True
