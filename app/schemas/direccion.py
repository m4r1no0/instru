from pydantic import BaseModel, Field
from typing import Optional


# ======================================
# BASE
# ======================================
class DireccionBase(BaseModel):
    id_instructor: int
    municipio: str = Field(..., min_length=2, max_length=30)
    barrio: str = Field(..., min_length=2, max_length=30)
    complemento: str = Field(..., min_length=2, max_length=50)


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
class DireccionOut(DireccionBase):
    id_direccion: int

    class Config:
        from_attributes = True
