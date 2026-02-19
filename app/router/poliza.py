from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.poliza import (
    PolizaCreate,
    PolizaUpdate,
    PolizaOut,
    PolizaWithInstructor
)
from app.crud import poliza as poliza_crud


router = APIRouter()


# =====================================
# CREAR
# =====================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_poliza(
    poliza: PolizaCreate,
    db: Session = Depends(get_db)
):
    if poliza_crud.get_poliza_by_numero(
        db,
        poliza.numero_poliza
    ):
        raise HTTPException(
            status_code=400,
            detail="El número de póliza ya existe"
        )

    poliza_crud.create_poliza(db, poliza)

    return {"message": "Póliza creada correctamente"}


# =====================================
# LISTAR TODAS
# =====================================
@router.get("/", response_model=List[PolizaWithInstructor])
def get_all_polizas(db: Session = Depends(get_db)):
    return poliza_crud.get_all_polizas(db)


# =====================================
# LISTAR POR INSTRUCTOR
# =====================================
@router.get("/instructor/{id_instructor}",
            response_model=List[PolizaOut])
def get_polizas_por_instructor(
    id_instructor: int,
    db: Session = Depends(get_db)
):
    return poliza_crud.get_polizas_by_instructor(
        db,
        id_instructor
    )


# =====================================
# ACTUALIZAR
# =====================================
@router.put("/{id_poliza}")
def update_poliza(
    id_poliza: int,
    poliza: PolizaUpdate,
    db: Session = Depends(get_db)
):
    updated = poliza_crud.update_poliza(
        db,
        id_poliza,
        poliza
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Póliza no encontrada"
        )

    return {"message": "Póliza actualizada correctamente"}


# =====================================
# ELIMINAR
# =====================================
@router.delete("/{id_poliza}")
def delete_poliza(
    id_poliza: int,
    db: Session = Depends(get_db)
):
    deleted = poliza_crud.delete_poliza(
        db,
        id_poliza
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Póliza no encontrada"
        )

    return {"message": "Póliza eliminada correctamente"}
