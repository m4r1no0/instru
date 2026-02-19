from pydantic import BaseModel, Field
from typing import Optional


# =====================================
# BASE
# =====================================
class AreaFormacionBase(BaseModel):
    id_programa: int
    nombre_area: str = Field(..., max_length=150)
    objeto: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = None


# =====================================
# CREAR
# =====================================
class AreaFormacionCreate(AreaFormacionBase):
    pass


# =====================================
# ACTUALIZAR
# =====================================
class AreaFormacionUpdate(BaseModel):
    nombre_area: Optional[str] = Field(default=None, max_length=150)
    objeto: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = None


# =====================================
# RESPUESTA SIMPLE
# =====================================
class AreaFormacionOut(AreaFormacionBase):
    id_area: int

    class Config:
        from_attributes = True


# =====================================
# RESPUESTA CON PROGRAMA
# =====================================
class AreaFormacionWithPrograma(BaseModel):
    id_area: int
    id_programa: int
    nombre_programa: str
    nombre_area: str
    objeto: Optional[str]
    descripcion: Optional[str]

    class Config:
        from_attributes = True
