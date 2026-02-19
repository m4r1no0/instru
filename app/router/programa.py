from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.programa import (
    ProgramaCreate,
    ProgramaUpdate,
    ProgramaOut
)
from app.crud import programa as programa_crud


router = APIRouter()


# =====================================
# CREAR
# =====================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_programa(
    programa: ProgramaCreate,
    db: Session = Depends(get_db)
):
    # Validar código único
    if programa_crud.get_programa_by_codigo(
        db,
        programa.codigo_programa
    ):
        raise HTTPException(
            status_code=400,
            detail="El código del programa ya existe"
        )

    programa_crud.create_programa(db, programa)

    return {"message": "Programa creado correctamente"}


# =====================================
# OBTENER POR ID
# =====================================
@router.get("/{id_programa}",
            response_model=ProgramaOut)
def get_programa(
    id_programa: int,
    db: Session = Depends(get_db)
):
    programa = programa_crud.get_programa_by_id(
        db,
        id_programa
    )

    if not programa:
        raise HTTPException(
            status_code=404,
            detail="Programa no encontrado"
        )

    return programa


# =====================================
# LISTAR TODOS
# =====================================
@router.get("/", response_model=List[ProgramaOut])
def get_all_programas(
    db: Session = Depends(get_db)
):
    return programa_crud.get_all_programas(db)


# =====================================
# ACTUALIZAR
# =====================================
@router.put("/{id_programa}")
def update_programa(
    id_programa: int,
    programa: ProgramaUpdate,
    db: Session = Depends(get_db)
):
    updated = programa_crud.update_programa(
        db,
        id_programa,
        programa
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Programa no encontrado"
        )

    return {"message": "Programa actualizado correctamente"}
