from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.contrato import (
    ContratoCreate,
    ContratoUpdate,
    ContratoOut
)
from app.crud import contrato as contrato_crud

router = APIRouter()


# ======================================
# CREAR CONTRATO
# ======================================
@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
def create_contrato(
    contrato: ContratoCreate,
    db: Session = Depends(get_db)
):
    created = contrato_crud.create_contrato(db, contrato)

    if not created:
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear el contrato"
        )

    return {"message": "Contrato creado correctamente"}


# ======================================
# OBTENER CONTRATO POR ID
# ======================================
@router.get(
    "/{id_contrato}",
    response_model=ContratoOut
)
def get_contrato(
    id_contrato: int,
    db: Session = Depends(get_db)
):
    contrato = contrato_crud.get_contrato_by_id(db, id_contrato)

    if not contrato:
        raise HTTPException(
            status_code=404,
            detail="Contrato no encontrado"
        )

    return contrato


# ======================================
# LISTAR TODOS LOS CONTRATOS
# ======================================
@router.get(
    "/",
    response_model=List[ContratoOut]
)
def get_all_contratos(
    db: Session = Depends(get_db)
):
    return contrato_crud.get_all_contratos(db)


# ======================================
# LISTAR CONTRATOS POR INSTRUCTOR
# ======================================
@router.get(
    "/instructor/{id_instructor}",
    response_model=List[ContratoOut]
)
def get_contratos_by_instructor(
    id_instructor: int,
    db: Session = Depends(get_db)
):
    return contrato_crud.get_contratos_by_instructor(
        db,
        id_instructor
    )


# ======================================
# ACTUALIZAR CONTRATO
# ======================================
@router.put(
    "/{id_contrato}",
    response_model=dict
)
def update_contrato(
    id_contrato: int,
    contrato: ContratoUpdate,
    db: Session = Depends(get_db)
):
    updated = contrato_crud.update_contrato(
        db,
        id_contrato,
        contrato
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Contrato no encontrado o sin cambios"
        )

    return {"message": "Contrato actualizado correctamente"}


# ======================================
# ELIMINAR CONTRATO
# ======================================
@router.delete(
    "/{id_contrato}",
    response_model=dict
)
def delete_contrato(
    id_contrato: int,
    db: Session = Depends(get_db)
):
    deleted = contrato_crud.delete_contrato(
        db,
        id_contrato
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Contrato no encontrado"
        )

    return {"message": "Contrato eliminado correctamente"}
