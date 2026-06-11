from pydantic import BaseModel
from typing import Optional
from datetime import date


class CesionBase(BaseModel):
    id_contrato: int
    id_instructor: int
    id_usuario: int
    fecha_incio: Optional[date] = None
    fecha_cesion: Optional[date] = None
    fecha_modificacion: Optional[date] = None


class CesionCreate(CesionBase):
    pass


class CesionUpdate(BaseModel):
    id_contrato: Optional[int] = None
    id_instructor: Optional[int] = None
    id_usuario: Optional[int] = None
    fecha_incio: Optional[date] = None
    fecha_cesion: Optional[date] = None
    fecha_modificacion: Optional[date] = None


class CesionOut(CesionBase):
    id_modificacion: int

    class Config:
        from_attributes = True


class CesionWithRelations(BaseModel):
    id_modificacion: int
    id_contrato: int
    numero_contrato: Optional[str] = None
    id_instructor: int
    instructor_nombres: Optional[str] = None
    instructor_apellidos: Optional[str] = None
    id_usuario: int
    usuario_nombre: Optional[str] = None
    fecha_incio: Optional[date] = None
    fecha_cesion: Optional[date] = None
    fecha_modificacion: Optional[date] = None
