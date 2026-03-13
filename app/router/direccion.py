from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.direccion import (
    DireccionCreate,
    DireccionUpdate,
    DireccionOut
)
from app.crud import direccion as direccion_crud


router = APIRouter()


# ======================================
# LISTAR TODAS LAS DIRECCIONES (DEBE IR PRIMERO)
# ======================================
@router.get("/all", response_model=List[DireccionOut])
def get_all_direcciones(
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las direcciones
    """
    direcciones = direccion_crud.get_all_direcciones(db)
    return direcciones


# ======================================
# LISTAR POR INSTRUCTOR (ESPECÍFICO)
# ======================================
@router.get("/instructor/{id_instructor}", response_model=List[DireccionOut])
def get_direcciones_by_instructor(
    id_instructor: int,
    db: Session = Depends(get_db)
):
    return direccion_crud.get_direcciones_by_instructor(db, id_instructor)


# ======================================
# OBTENER POR ID (DEBE IR DESPUÉS DE RUTAS ESPECÍFICAS)
# ======================================
@router.get("/{id_direccion}", response_model=DireccionOut)
def get_direccion(
    id_direccion: int,
    db: Session = Depends(get_db)
):
    direccion = direccion_crud.get_direccion_by_id(db, id_direccion)

    if not direccion:
        raise HTTPException(
            status_code=404,
            detail="Dirección no encontrada"
        )

    return direccion


# ======================================
# CREAR
# ======================================
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_direccion(
    direccion: DireccionCreate,
    db: Session = Depends(get_db)
):
    if not direccion_crud.create_direccion(db, direccion):
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear la dirección"
        )

    return {"message": "Dirección creada correctamente"}


# ======================================
# ACTUALIZAR
# ======================================
@router.put("/{id_direccion}")
def update_direccion(
    id_direccion: int,
    direccion: DireccionUpdate,
    db: Session = Depends(get_db)
):
    updated = direccion_crud.update_direccion(db, id_direccion, direccion)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Dirección no encontrada o sin cambios"
        )

    return {"message": "Dirección actualizada correctamente"}


# ======================================
# ELIMINAR
# ======================================
@router.delete("/{id_direccion}")
def delete_direccion(
    id_direccion: int,
    db: Session = Depends(get_db)
):
    deleted = direccion_crud.delete_direccion(db, id_direccion)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Dirección no encontrada"
        )

    return {"message": "Dirección eliminada correctamente"}