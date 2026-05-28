from pydantic import BaseModel, Field
from typing import Optional, Union
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
    valor_contrato: Optional[Union[Decimal, str, float]] = None
    valorAdDi : Optional[Decimal] = None
    valor_mes : Optional[Decimal] = None
    valor_mes_inicial: Optional[Decimal] = None
    valor_mes_final: Optional[Decimal] = None
    estado: Optional[str] = Field(default=None, max_length=30)
    cdp: Optional[str] 
    crp: Optional[str] 
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
    valor_mes: Optional[Union[Decimal, str, float]] = None  # Aceptar múltiples tipos
    valorAdDi : Optional[Union[Decimal, str, float]] = None
    valor_mes_inicial: Optional[Union[Decimal, str, float]] = None
    valor_mes_final: Optional[Union[Decimal, str, float]] = None
    estado: Optional[str] = Field(default=None, max_length=30)
    cdp: Optional[str]
    crp: Optional[str] 
    rubro: Optional[str] = Field(default=None, max_length=100)
    dependencia: Optional[str] = Field(default=None, max_length=100)


# =========================================
# RESPUESTA
# =========================================
class ContratoOut(ContratoBase):
    id_contrato: int

class InstructorContratoOut(BaseModel):
    """Schema para la consulta que une instructores con sus contratos"""
    nombres: str = Field(..., description="Nombres del instructor")
    apellidos: str = Field(..., description="Apellidos del instructor")
    numero_contrato: Optional[str] = Field(None, description="Número de contrato (puede ser NULL si el instructor no tiene contrato)")
    crp: Optional[int] = Field(None, description="CRP del contrato (puede ser NULL si el instructor no tiene contrato)")
    numero_documento: Optional[int]
    supervisor_nombres: Optional[str] = Field(None, description="Nombres del supervisor (puede ser NULL si no tiene supervisor)")


class ContratoInstructorPago(BaseModel):
    nombre_completo: str
    numero_contrato: Optional[str]
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    vigencia: Optional[date]
    valor_mes: Optional[Decimal]
    valor_contrato: Optional[Decimal]
    valor_mes_inicial: Optional[Decimal]
    valor_mes_final: Optional[Decimal]
    valorAdDi: Optional[Decimal]

    