from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from app.schemas.pago import (
    PagoCreate,
    PagoUpdate,
    PagoOut,
    ReportePagosPorInstructor,
    ReportePagosPorMes,
)
from app.crud import pago as pago_crud

router = APIRouter()


# =====================================
# LISTAR TODOS LOS PAGOS
# =====================================
@router.get("/all", response_model=List[PagoOut])
def get_all_pagos(db: Session = Depends(get_db)):
    """Lista todos los pagos"""
    result = pago_crud.get_all_pagos(db)
    return result


# =====================================
# LISTAR PAGOS POR CONTRATO
# =====================================
@router.get("/contrato/{id_contrato}", response_model=List[PagoOut])
def get_pagos_by_contrato(id_contrato: int, db: Session = Depends(get_db)):
    """Lista pagos por contrato"""
    pagos = pago_crud.get_pagos_by_contrato(db, id_contrato)
    return pagos


# =====================================
# LISTAR PAGOS POR INSTRUCTOR
# =====================================
@router.get("/instructor/{id_instructor}", response_model=List[PagoOut])
def get_pagos_by_instructor(id_instructor: int, db: Session = Depends(get_db)):
    """Lista pagos por instructor"""
    pagos = pago_crud.get_pagos_by_instructor(db, id_instructor)
    return pagos


# =====================================
# CREAR PAGO
# =====================================
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    if not pago_crud.create_pago(db, pago):
        raise HTTPException(status_code=400, detail="No se pudo crear el pago")
    return {"message": "Pago creado correctamente"}


# =====================================
# OBTENER PAGO POR ID
# =====================================
@router.get("/{id_pago}", response_model=PagoOut)
def get_pago(id_pago: int, db: Session = Depends(get_db)):
    pago = pago_crud.get_pago_by_id(db, id_pago)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago


# =====================================
# ACTUALIZAR PAGO
# =====================================
@router.put("/{id_pago}")
def update_pago(id_pago: int, pago: PagoUpdate, db: Session = Depends(get_db)):
    updated = pago_crud.update_pago(db, id_pago, pago)
    if not updated:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return {"message": "Pago actualizado correctamente"}


# =====================================
# ELIMINAR PAGO
# =====================================
@router.delete("/{id_pago}")
def delete_pago(id_pago: int, db: Session = Depends(get_db)):
    deleted = pago_crud.delete_pago(db, id_pago)
    if not deleted:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return {"message": "Pago eliminado correctamente"}


# =====================================
# REPORTES
# =====================================
@router.get("/reportes/resumen-instructores")
def get_resumen_instructores(db: Session = Depends(get_db)):
    """Resumen de pagos por instructor"""
    result = pago_crud.get_resumen_pagos_por_instructor(db)
    return result


@router.get("/reportes/saldos-pendientes")
def get_saldos_pendientes(db: Session = Depends(get_db)):
    """Lista de pagos con saldo pendiente"""
    result = pago_crud.get_pagos_con_saldo_pendiente(db)
    return result
