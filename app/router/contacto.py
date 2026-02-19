from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.contacto import (
    ContactoCreate,
    ContactoUpdate,
    ContactoOut
)
from app.crud import contacto as contacto_crud


router = APIRouter()


# =====================================
# CREAR
# =====================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_contacto(
    contacto: ContactoCreate,
    db: Session = Depends(get_db)
):
    if not contacto_crud.create_contacto(db, contacto):
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear el contacto"
        )

    return {"message": "Contacto creado correctamente"}


# =====================================
# OBTENER POR ID
# =====================================
@router.get("/{id_contacto}", response_model=ContactoOut)
def get_contacto(
    id_contacto: int,
    db: Session = Depends(get_db)
):
    contacto = contacto_crud.get_contacto_by_id(db, id_contacto)

    if not contacto:
        raise HTTPException(
            status_code=404,
            detail="Contacto no encontrado"
        )

    return contacto


# =====================================
# LISTAR POR INSTRUCTOR
# =====================================
@router.get("/instructor/{id_instructor}",
            response_model=List[ContactoOut])
def get_contactos_by_instructor(
    id_instructor: int,
    db: Session = Depends(get_db)
):
    return contacto_crud.get_contactos_by_instructor(
        db,
        id_instructor
    )


# =====================================
# ACTUALIZAR
# =====================================
@router.put("/{id_contacto}")
def update_contacto(
    id_contacto: int,
    contacto: ContactoUpdate,
    db: Session = Depends(get_db)
):
    updated = contacto_crud.update_contacto(
        db,
        id_contacto,
        contacto
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Contacto no encontrado"
        )

    return {"message": "Contacto actualizado correctamente"}


# =====================================
# ELIMINAR
# =====================================
@router.delete("/{id_contacto}")
def delete_contacto(
    id_contacto: int,
    db: Session = Depends(get_db)
):
    deleted = contacto_crud.delete_contacto(
        db,
        id_contacto
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Contacto no encontrado"
        )

    return {"message": "Contacto eliminado correctamente"}
