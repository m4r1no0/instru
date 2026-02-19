from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.rol import (
    RolCreate,
    RolUpdate,
    RolOut
)
from app.crud import rol as rol_crud


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


# =====================================
# CREAR
# =====================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_rol(
    rol: RolCreate,
    db: Session = Depends(get_db)
):
    rol_crud.create_rol(db, rol)
    return {"message": "Rol creado correctamente"}


# =====================================
# OBTENER POR ID
# =====================================
@router.get("/{id_rol}", response_model=RolOut)
def get_rol(
    id_rol: int,
    db: Session = Depends(get_db)
):
    rol = rol_crud.get_rol_by_id(db, id_rol)

    if not rol:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return rol


# =====================================
# LISTAR TODOS
# =====================================
@router.get("/", response_model=List[RolOut])
def get_all_roles(
    db: Session = Depends(get_db)
):
    return rol_crud.get_all_roles(db)


# =====================================
# ACTUALIZAR
# =====================================
@router.put("/{id_rol}")
def update_rol(
    id_rol: int,
    rol: RolUpdate,
    db: Session = Depends(get_db)
):
    updated = rol_crud.update_rol(
        db,
        id_rol,
        rol
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return {"message": "Rol actualizado correctamente"}


# =====================================
# ELIMINAR
# =====================================
@router.delete("/{id_rol}")
def delete_rol(
    id_rol: int,
    db: Session = Depends(get_db)
):
    deleted = rol_crud.delete_rol(
        db,
        id_rol
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return {"message": "Rol eliminado correctamente"}
