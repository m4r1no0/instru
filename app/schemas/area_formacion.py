from pydantic import BaseModel, Field
from typing import Optional


# =====================================
# BASE
# =====================================
class AreaFormacionBase(BaseModel):
    id_area: Optional[int] = None  # Cambiado a Optional
    nombre_area: Optional[str] = Field(default=None, max_length=150)
    objeto: Optional[str] = Field(default=None)
    descripcion: Optional[str] = None


# =====================================
# CREAR
# =====================================
class AreaFormacionCreate(AreaFormacionBase):
    # Cuando creas un área, el id_area es obligatorio
    id_area: int
    nombre_area: str = Field(..., max_length=150)


# =====================================
# ACTUALIZAR
# =====================================
class AreaFormacionUpdate(BaseModel):
    nombre_area: Optional[str] = Field(default=None, max_length=150)
    objeto: Optional[str] = Field(default=None)
    descripcion: Optional[str] = None


# =====================================
# RESPUESTA SIMPLE
# =====================================
class AreaFormacionOut(AreaFormacionBase):
    id_area: Optional[int] = None  # Cambiado a Optional
    id_instructor: int
    nombre: str  # El nombre del instructor
    nombre_programa: Optional[str]
    nombre_supervisor: Optional[str]

    class Config:
        from_attributes = True


# =====================================
# RESPUESTA CON PROGRAMA
# =====================================
class AreaFormacionWithPrograma(BaseModel):
    id_area: Optional[int] = None  # Cambiado a Optional
    id_programa: int
    nombre_programa: str
    nombre_area: Optional[str] = None
    objeto: Optional[str] = None
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True