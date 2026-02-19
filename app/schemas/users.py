from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# ==========================
# BASE
# ==========================
class UserBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=80)
    id_rol: int
    email: EmailStr
    telefono: str = Field(min_length=7, max_length=15)
    documento: str = Field(min_length=8, max_length=20)
    estado: int   # Cambiado de bool a int (según tu BD)


# ==========================
# CREAR
# ==========================
class UserCreate(UserBase):
    password: str = Field(min_length=8)


# ==========================
# ACTUALIZAR
# ==========================
class UserUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=80)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(default=None, min_length=7, max_length=15)
    documento: Optional[str] = Field(default=None, min_length=8, max_length=20)
    password: Optional[str] = Field(default=None, min_length=8)


# ==========================
# CAMBIAR ESTADO
# ==========================
class UserEstado(BaseModel):
    estado: Optional[int] = None


# ==========================
# RESPUESTA
# ==========================
class UserOut(UserBase):
    id_usuario: int
    nombre_rol: str
