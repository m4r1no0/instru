from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.area_formacion import (
    AreaFormacionCreate,
    AreaFormacionUpdate,
    AreaFormacionOut,
    AreaFormacionWithPrograma
)
from app.crud import area_formacion as area_crud


router = APIRouter()


# =====================================
# CREAR
# =====================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_area(
    area: AreaFormacionCreate,
    db: Session = Depends(get_db)
):
    area_crud.create_area_formacion(db, area)
    return {"message": "Área creada correctamente"}


# =====================================
# OBTENER POR ID
# =====================================
@router.get("/{id_area}",
            response_model=AreaFormacionOut)
def get_area(
    id_area: int,
    db: Session = Depends(get_db)
):
    area = area_crud.get_area_by_id(db, id_area)

    if not area:
        raise HTTPException(
            status_code=404,
            detail="Área no encontrada"
        )

    return area


# =====================================
# LISTAR TODAS (CON PROGRAMA)
# =====================================
@router.get("/",
            response_model=List[AreaFormacionWithPrograma])
def get_all_areas(
    db: Session = Depends(get_db)
):
    return area_crud.get_all_areas(db)


# =====================================
# LISTAR POR PROGRAMA
# =====================================
@router.get("/programa/{id_programa}",
            response_model=List[AreaFormacionOut])
def get_areas_by_programa(
    id_programa: int,
    db: Session = Depends(get_db)
):
    return area_crud.get_areas_by_programa(
        db,
        id_programa
    )


# =====================================
# ACTUALIZAR
# =====================================
@router.put("/{id_area}")
def update_area(
    id_area: int,
    area: AreaFormacionUpdate,
    db: Session = Depends(get_db)
):
    updated = area_crud.update_area_formacion(
        db,
        id_area,
        area
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Área no encontrada"
        )

    return {"message": "Área actualizada correctamente"}


# =====================================
# ELIMINAR
# =====================================
@router.delete("/{id_area}")
def delete_area(
    id_area: int,
    db: Session = Depends(get_db)
):
    deleted = area_crud.delete_area_formacion(
        db,
        id_area
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Área no encontrada"
        )

    return {"message": "Área eliminada correctamente"}
