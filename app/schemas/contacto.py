# =====================================#
# BASE
# =====================================#
from typing import  Optional
from pydantic import BaseModel, Field


class ContactoBase(BaseModel):
    id_instructor: int = Field(gt=0, description="ID del instructor debe ser positivo")
    correo_personal: Optional[str] = None  # Usar EmailStr para validación
    correo_institucional: Optional[str] = None
    telefono: Optional[str] = None

# =====================================
# CREAR
# =====================================
class ContactoCreate(ContactoBase):
    pass


class ContactoUpdate(ContactoBase):
    correo_personal: Optional[str] = None
    correo_institucional: Optional[str] = None
    telefono: Optional[str] = None


# =====================================
# RESPUESTA
# =====================================
class ContactoOut(BaseModel):
    id_contacto: Optional[int] = None
    id_instructor: Optional[int] = None
    nombre: Optional[str] = None  # Renombrado para claridad
    correo_personal: Optional[str] = None
    correo_institucional: Optional[str] = None
    telefono: Optional[str] = None
    
    class Config:
        from_attributes = True
