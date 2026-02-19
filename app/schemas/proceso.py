from pydantic import BaseModel, HttpUrl
from typing import Optional


# =====================================
# BASE
# =====================================
class ProcesoBase(BaseModel):
    id_contrato: int
    numero_proceso: Optional[str] = None
    informe_final: Optional[str] = None
    paz_y_salvo: Optional[str] = None
    link_secop: Optional[str] = None


# =====================================
# CREAR
# =====================================
class ProcesoCreate(ProcesoBase):
    pass


# =====================================
# ACTUALIZAR
# =====================================
class ProcesoUpdate(BaseModel):
    numero_proceso: Optional[str] = None
    informe_final: Optional[str] = None
    paz_y_salvo: Optional[str] = None
    link_secop: Optional[str] = None


# =====================================
# RESPUESTA NORMAL
# =====================================
class ProcesoOut(ProcesoBase):
    id_proceso: int

    class Config:
        from_attributes = True


# =====================================
# RESPUESTA CON INSTRUCTOR
# =====================================
class ProcesoWithInstructor(BaseModel):
    id_proceso: int
    id_contrato: int
    id_instructor: int
    numero_proceso: Optional[str]
    informe_final: Optional[str]
    paz_y_salvo: Optional[str]
    link_secop: Optional[str]

    class Config:
        from_attributes = True
