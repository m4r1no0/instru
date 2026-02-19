from pydantic import BaseModel, Field
from typing import Optional


# =====================================
# BASE
# =====================================
class ProgramaBase(BaseModel):
    codigo_programa: str = Field(..., max_length=30)
    nombre_programa: str = Field(..., max_length=150)
    nivel_formacion: Optional[str] = Field(default=None, max_length=50)
    modalidad: Optional[str] = Field(default=None, max_length=50)


# =====================================
# CREAR
# =====================================
class ProgramaCreate(ProgramaBase):
    pass


# =====================================
# ACTUALIZAR
# =====================================
class ProgramaUpdate(BaseModel):
    codigo_programa: Optional[str] = Field(default=None, max_length=30)
    nombre_programa: Optional[str] = Field(default=None, max_length=150)
    nivel_formacion: Optional[str] = Field(default=None, max_length=50)
    modalidad: Optional[str] = Field(default=None, max_length=50)


# =====================================
# RESPUESTA
# =====================================
class ProgramaOut(ProgramaBase):
    id_programa: int

    class Config:
        from_attributes = True
