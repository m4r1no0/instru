# =====================================#
# BASE
# =====================================#
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class PagoBase(BaseModel):
    id_contrato: int = Field(gt=0, description="ID del contrato")
    mes: str = Field(..., max_length=20, description="Mes en formato YYYY-MM")
    valor_base: Decimal = Field(..., gt=0, decimal_places=2, description="Valor base del mes")
    ajuste: Optional[Decimal] = Field(0, decimal_places=2, description="Ajuste (bono/descuento)")
    valor_pagado: Decimal = Field(..., ge=0, decimal_places=2, description="Valor pagado")
    saldo: Optional[Decimal] = Field(0, decimal_places=2, description="Saldo pendiente")

    @field_validator("mes")
    @classmethod
    def validar_mes(cls, v):
        import re
        if not re.match(r"^\d{4}-\d{2}$", v):
            raise ValueError("El mes debe tener formato YYYY-MM (ej: 2024-10)")
        año, mes = map(int, v.split('-'))
        if mes < 1 or mes > 12:
            raise ValueError("El mes debe estar entre 01 y 12")
        return v

    @field_validator("valor_pagado")
    @classmethod
    def validar_valor_pagado(cls, v, info):
        if v < 0:
            raise ValueError("El valor pagado no puede ser negativo")
        return v

# =====================================
# CREAR
# =====================================
class PagoCreate(PagoBase):
    pass

# =====================================
# ACTUALIZAR
# =====================================
class PagoUpdate(BaseModel):
    id_contrato: Optional[int] = Field(None, gt=0)
    mes: Optional[str] = Field(None, max_length=20)
    valor_base: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    ajuste: Optional[Decimal] = Field(None, decimal_places=2)
    valor_pagado: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    saldo: Optional[Decimal] = Field(None, decimal_places=2)

    @field_validator("mes")
    @classmethod
    def validar_mes(cls, v):
        if v:
            import re
            if not re.match(r"^\d{4}-\d{2}$", v):
                raise ValueError("El mes debe tener formato YYYY-MM (ej: 2024-10)")
            año, mes = map(int, v.split('-'))
            if mes < 1 or mes > 12:
                raise ValueError("El mes debe estar entre 01 y 12")
        return v

# =====================================
# RESPUESTA
# =====================================
class PagoOut(BaseModel):
    id_pago: int
    id_contrato: int
    numero_contrato: Optional[str] = None
    instructor_nombre: Optional[str] = None
    mes: str
    valor_base: Decimal
    ajuste: Decimal
    valor_pagado: Decimal
    saldo: Decimal
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# =====================================
# REPORTES
# =====================================
class ReportePagosPorInstructor(BaseModel):
    id_instructor: int
    instructor_nombre: str
    total_contratos: int
    total_valor_base: Decimal
    total_ajustes: Decimal
    total_pagado: Decimal
    total_saldo: Decimal

class ReportePagosPorMes(BaseModel):
    mes: str
    total_pagos: int
    total_valor_base: Decimal
    total_pagado: Decimal
    total_saldo: Decimal