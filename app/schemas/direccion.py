from pydantic import BaseModel, Field
from typing import Optional


# ======================================
# BASE
# ======================================
class DireccionBase(BaseModel):
    id_instructor: int
    municipio: str = Field(..., min_length=2, max_length=30)
    barrio: str = Field(..., min_length=2, max_length=30)
    complemento: str = Field(..., min_length=2)



# ======================================
# CREAR
# ======================================
class DireccionCreate(DireccionBase):
    pass


# ======================================
# ACTUALIZAR
# ======================================
class DireccionUpdate(BaseModel):
    municipio: Optional[str] = Field(default=None, min_length=2, max_length=30)
    barrio: Optional[str] = Field(default=None, min_length=2, max_length=30)
    complemento: Optional[str] = Field(default=None, min_length=2, max_length=50)


# ======================================
# RESPUESTA
# ======================================    
class DireccionOut(BaseModel):
    id_instructor: int
    id_direccion: int
    nombre: Optional[str] = None  # ← Cambiado de 'nombres' a 'nombre'
    municipio: str
    complemento: str
    telefono: Optional[str] = None  # ← Agregado
    correo_personal: Optional[str] = None  # ← Agregado
    # barrio se elimina porque no está en el SELECT
    
    class Config:
        from_attributes = True