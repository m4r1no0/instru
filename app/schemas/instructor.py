from datetime import date
from pydantic import BaseModel, ConfigDict, Field
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
    id_supervisor: Optional[int] = None  # Opcional

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
    id_instructor: int
    tipo_documento: str
    numero_documento: int
    nombres: str
    apellidos: str
    fecha_nacimiento: Optional[date] = None
    fecha_expedicion: Optional[date] = None
    arl: Optional[str] = None
    id_supervisor: Optional[int] = None