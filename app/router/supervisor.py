from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.supervisor import (
    SupervisorCreate,
    SupervisorUpdate,
    SupervisorOut
)
from app.crud import supervisor as supervisor_crud


router = APIRouter()


# =====================================
# CREAR
# =====================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_supervisor(
    supervisor: SupervisorCreate,
    db: Session = Depends(get_db)
):
    supervisor_crud.create_supervisor(db, supervisor)

    return {"message": "Supervisor creado correctamente"}


# =====================================
# OBTENER POR ID
# =====================================
@router.get("/{id_supervisor}",
            response_model=SupervisorOut)
def get_supervisor(
    id_supervisor: int,
    db: Session = Depends(get_db)
):
    supervisor = supervisor_crud.get_supervisor_by_id(
        db,
        id_supervisor
    )

    if not supervisor:
        raise HTTPException(
            status_code=404,
            detail="Supervisor no encontrado"
        )

    return supervisor


# =====================================
# LISTAR TODOS
# =====================================
@router.get("/", response_model=List[SupervisorOut])
def get_all_supervisores(
    db: Session = Depends(get_db)
):
    return supervisor_crud.get_all_supervisores(db)


# =====================================
# ACTUALIZAR
# =====================================
@router.put("/{id_supervisor}")
def update_supervisor(
    id_supervisor: int,
    supervisor: SupervisorUpdate,
    db: Session = Depends(get_db)
):
    updated = supervisor_crud.update_supervisor(
        db,
        id_supervisor,
        supervisor
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Supervisor no encontrado"
        )

    return {"message": "Supervisor actualizado correctamente"}


# =====================================
# ELIMINAR
# =====================================
@router.delete("/{id_supervisor}")
def delete_supervisor(
    id_supervisor: int,
    db: Session = Depends(get_db)
):
    deleted = supervisor_crud.delete_supervisor(
        db,
        id_supervisor
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Supervisor no encontrado"
        )

    return {"message": "Supervisor eliminado correctamente"}
