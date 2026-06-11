from datetime import date
from pydantic import BaseModel, Field
from typing import Optional


# 🔹 Campos comunes
class InstructorBase(BaseModel):
    tipo_documento: str
    numero_documento: int  # Ahora es int
    nombres: str = Field(min_length=3, max_length=80)
    apellidos: str = Field(min_length=3, max_length=50)
    fecha_nacimiento: Optional[date] = None
    fecha_expedicion: Optional[date] = None
    arl: Optional[str] = None
    id_supervisor: Optional[int] = None


# 🔹 Para crear (NO incluye id)
class InstructorCreate(InstructorBase):
    pass


# 🔹 Para actualizar (campos opcionales)
class InstructorUpdate(BaseModel):
    tipo_documento: Optional[str] = None
    numero_documento: Optional[int] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    fecha_expedicion: Optional[date] = None
    arl: Optional[str] = None
    id_supervisor: Optional[int] = None


# 🔹 Para devolver al frontend (SÍ incluye id)
class InstructorOut(BaseModel):
    # Campos de instructor
    id_instructor: int
    tipo_documento: str
    numero_documento: int
    nombres: str
    fecha_nacimiento: Optional[date] = None
    fecha_expedicion: Optional[date] = None
    arl: Optional[str] = None  # CONCAT(i.nombres, ' ', i.apellidos)

    # Campos de supervisor
    id_supervisor: Optional[int] = None
    nombre: Optional[str] = None  # s.nombre (nombre del supervisor)

    # Campos de contrato
    numero_contrato: Optional[str] = None
    crp: Optional[str] = None
    cdp: Optional[str] = None
    estado: Optional[str] = None
    valor_contrato: Optional[float] = None
    valor_mes: Optional[float] = None
    valorAdDi: Optional[float] = None
    rubro: Optional[str] = None
    dependencia: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

    # campo de programa_formacion
    nombre_programa: Optional[str] = None
    nombre_area: Optional[str] = None

    class Config:
        from_attributes = True
