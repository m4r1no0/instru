from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.proceso import (
    ProcesoCreate,
    ProcesoUpdate,
    ProcesoOut,
    ProcesoWithInstructor
)
from app.crud import proceso as proceso_crud


router = APIRouter()


# =====================================
# CREAR
# =====================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_proceso(
    proceso: ProcesoCreate,
    db: Session = Depends(get_db)
):
    if not proceso_crud.create_proceso(db, proceso):
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear el proceso"
        )

    return {"message": "Proceso creado correctamente"}


# =====================================
# OBTENER POR ID
# =====================================
@router.get("/{id_proceso}", response_model=ProcesoOut)
def get_proceso(
    id_proceso: int,
    db: Session = Depends(get_db)
):
    proceso = proceso_crud.get_proceso_by_id(db, id_proceso)

    if not proceso:
        raise HTTPException(
            status_code=404,
            detail="Proceso no encontrado"
        )

    return proceso


# =====================================
# LISTAR TODOS (con instructor)
# =====================================
@router.get("/", response_model=List[ProcesoWithInstructor])
def get_all_procesos(db: Session = Depends(get_db)):
    return proceso_crud.get_all_procesos(db)


# =====================================
# LISTAR POR CONTRATO
# =====================================
@router.get("/contrato/{id_contrato}",
            response_model=List[ProcesoOut])
def get_procesos_by_contrato(
    id_contrato: int,
    db: Session = Depends(get_db)
):
    return proceso_crud.get_procesos_by_contrato(
        db,
        id_contrato
    )


# =====================================
# ACTUALIZAR
# =====================================
@router.put("/{id_proceso}")
def update_proceso(
    id_proceso: int,
    proceso: ProcesoUpdate,
    db: Session = Depends(get_db)
):
    updated = proceso_crud.update_proceso(
        db,
        id_proceso,
        proceso
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Proceso no encontrado"
        )

    return {"message": "Proceso actualizado correctamente"}


# =====================================
# ELIMINAR
# =====================================
@router.delete("/{id_proceso}")
def delete_proceso(
    id_proceso: int,
    db: Session = Depends(get_db)
):
    deleted = proceso_crud.delete_proceso(
        db,
        id_proceso
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Proceso no encontrado"
        )

    return {"message": "Proceso eliminado correctamente"}
