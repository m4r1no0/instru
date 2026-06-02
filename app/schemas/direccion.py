from pydantic import BaseModel, Field
from typing import Optional


# ======================================
# BASE
# ======================================
class DireccionBase(BaseModel):
    id_instructor: int
    municipio: str = Field(..., min_length=2, max_length=30)
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
    complemento: Optional[str] = Field(default=None, min_length=2, max_length=50)


# ======================================
# RESPUESTA
# ======================================    
class DireccionOut(BaseModel):
    id_instructor: int
    nombre: Optional[str] = None 
    id_direccion: Optional[int] = None  # ← Permitir None
    municipio: Optional[str] = None      # ← Permitir None
    complemento: Optional[str] = None    # ← Permitir None
    telefono: Optional[str] = None       # ← Permitir None
    correo_personal: Optional[str] = None
    correo_institucional: Optional[str] = None
    
    class Config:
        from_attributes = True
        