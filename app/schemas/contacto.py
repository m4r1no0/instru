from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re


# =====================================#
# BASE
# =====================================#
class ContactoBase(BaseModel):
    id_instructor: int
    correo_personal: Optional[EmailStr] = None
    correo_institucional: Optional[EmailStr] = None
    telefono: Optional[str] = None

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, v):
        if v is None:
            return v

        if not re.fullmatch(r"^\d{7,10}$", v):
            raise ValueError(
                "El teléfono debe contener solo números y entre 7 y 10 dígitos"
            )

        return v


# =====================================
# CREAR
# =====================================
class ContactoCreate(ContactoBase):
    pass


# =====================================
# ACTUALIZAR
# =====================================
class ContactoUpdate(BaseModel):
    correo_personal: Optional[EmailStr] = None
    correo_institucional: Optional[EmailStr] = None
    telefono: Optional[str] = Field(default=None, max_length=10)


# =====================================
# RESPUESTA
# =====================================
class ContactoOut(ContactoBase):
    id_contacto: int

    class Config:
        from_attributes = True
