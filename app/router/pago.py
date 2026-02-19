from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.pago import PagoCreate, PagoUpdate, PagoOut
from app.crud import pago as pago_crud


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_pago(
    pago: PagoCreate,
    db: Session = Depends(get_db)
):
    if not pago_crud.create_pago(db, pago):
        raise HTTPException(status_code=400, detail="No se pudo crear el pago")

    return {"message": "Pago creado correctamente"}


@router.get("/", response_model=List[PagoOut])
def get_all_pagos(db: Session = Depends(get_db)):
    return pago_crud.get_all_pagos(db)


@router.get("/{id_pago}", response_model=PagoOut)
def get_pago(id_pago: int, db: Session = Depends(get_db)):
    pago = pago_crud.get_pago_by_id(db, id_pago)

    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    return pago


@router.get("/contrato/{id_contrato}", response_model=List[PagoOut])
def get_pagos_by_contrato(id_contrato: int, db: Session = Depends(get_db)):
    return pago_crud.get_pagos_by_contrato(db, id_contrato)


@router.put("/{id_pago}")
def update_pago(
    id_pago: int,
    pago: PagoUpdate,
    db: Session = Depends(get_db)
):
    updated = pago_crud.update_pago(db, id_pago, pago)

    if not updated:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    return {"message": "Pago actualizado correctamente"}


@router.delete("/{id_pago}")
def delete_pago(id_pago: int, db: Session = Depends(get_db)):
    deleted = pago_crud.delete_pago(db, id_pago)

    if not deleted:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    return {"message": "Pago eliminado correctamente"}
