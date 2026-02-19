from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


# =====================================
# BASE
# =====================================
class PagoBase(BaseModel):
    id_contrato: int
    mes: Optional[str] = Field(default=None, max_length=20)
    valor_base: Decimal
    ajuste: Optional[Decimal] = 0
    valor_pagado: Decimal
    saldo: Optional[Decimal] = None


# =====================================
# CREAR
# =====================================
class PagoCreate(PagoBase):
    pass


# =====================================
# ACTUALIZAR
# =====================================
class PagoUpdate(BaseModel):
    mes: Optional[str] = Field(default=None, max_length=20)
    valor_base: Optional[Decimal] = None
    ajuste: Optional[Decimal] = None
    valor_pagado: Optional[Decimal] = None
    saldo: Optional[Decimal] = None


# =====================================
# RESPUESTA (incluye id_instructor)
# =====================================
class PagoOut(PagoBase):
    id_pago: int
    id_instructor: int   # 🔥 Lo agregamos desde el JOIN

    class Config:
        from_attributes = True
