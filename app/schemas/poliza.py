from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


# =====================================
# BASE
# =====================================
class PolizaBase(BaseModel):
    id_instructor: int
    numero_poliza: str = Field(..., max_length=50)
    tipo_poliza: str = Field(..., max_length=100)
    aseguradora: str = Field(..., max_length=150)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    valor_asegurado: Optional[Decimal] = None
    documento_pdf: Optional[str] = Field(default=None, max_length=255)
    observaciones: Optional[str] = None


# =====================================
# CREAR
# =====================================
class PolizaCreate(PolizaBase):
    pass


# =====================================
# ACTUALIZAR
# =====================================
class PolizaUpdate(BaseModel):
    numero_poliza: Optional[str] = Field(default=None, max_length=50)
    tipo_poliza: Optional[str] = Field(default=None, max_length=100)
    aseguradora: Optional[str] = Field(default=None, max_length=150)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    valor_asegurado: Optional[Decimal] = None
    documento_pdf: Optional[str] = Field(default=None, max_length=255)
    observaciones: Optional[str] = None
    estado: Optional[str] = Field(default=None, max_length=30)


# =====================================
# RESPUESTA
# =====================================
class PolizaOut(PolizaBase):
    id_poliza: int
    estado: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# =====================================
# RESPUESTA CON INSTRUCTOR
# =====================================
class PolizaWithInstructor(BaseModel):
    id_poliza: int
    numero_poliza: str
    tipo_poliza: str
    aseguradora: str
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    valor_asegurado: Optional[Decimal]
    estado: Optional[str]
    nombres: str
    apellidos: str

    class Config:
        from_attributes = True
