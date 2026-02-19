from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal


# =========================================
# BASE
# =========================================
class ContratoBase(BaseModel):
    id_instructor: int
    numero_contrato: str = Field(..., min_length=3, max_length=50)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    vigencia: Optional[date] = None
    valor_contrato: Optional[Decimal] = None
    estado: Optional[str] = Field(default=None, max_length=30)
    cdp: Optional[str] = Field(default=None, max_length=50)
    crp: Optional[str] = Field(default=None, max_length=50)
    rubro: Optional[str] = Field(default=None, max_length=100)
    dependencia: Optional[str] = Field(default=None, max_length=100)


# =========================================
# CREAR
# =========================================
class ContratoCreate(ContratoBase):
    pass


# =========================================
# ACTUALIZAR
# =========================================
class ContratoUpdate(BaseModel):
    id_instructor: Optional[int] = None
    numero_contrato: Optional[str] = Field(default=None, min_length=3, max_length=50)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    vigencia: Optional[date] = None
    valor_contrato: Optional[Decimal] = None
    estado: Optional[str] = Field(default=None, max_length=30)
    cdp: Optional[str] = Field(default=None, max_length=50)
    crp: Optional[str] = Field(default=None, max_length=50)
    rubro: Optional[str] = Field(default=None, max_length=100)
    dependencia: Optional[str] = Field(default=None, max_length=100)


# =========================================
# RESPUESTA
# =========================================
class ContratoOut(ContratoBase):
    id_contrato: int

    class Config:
        from_attributes = True
