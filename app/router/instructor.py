from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import text

from core.database import get_db
from app.schemas.instructor import (
    InstructorCreate,
    InstructorUpdate,
)
from app.crud import instructor as instructor_crud


router = APIRouter(
    prefix="/instructores",
    tags=["Instructores"]
)

# ==========================
# CREAR INSTRUCTOR
# ==========================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_instructor(
    instructor: InstructorCreate,
    db: Session = Depends(get_db)
):
    result = instructor_crud.create_instructor(db, instructor)

    if not result:
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear el instructor"
        )

    return {"message": "Instructor creado correctamente"}


# ==========================
# OBTENER POR ID
# ==========================
@router.get("/{id_instructor}")
def get_instructor_by_id(
    id_instructor: int,
    db: Session = Depends(get_db)
):
    instructor = instructor_crud.get_user_by_id(db, id_instructor)

    if not instructor:
        raise HTTPException(
            status_code=404,
            detail="Instructor no encontrado"
        )

    return instructor


# ==========================
# ACTUALIZAR INSTRUCTOR
# ==========================
@router.put("/{id_instructor}")
def update_instructor(
    id_instructor: int,
    instructor: InstructorUpdate,
    db: Session = Depends(get_db)
):
    updated = instructor_crud.update_user_by_id(
        db,
        id_instructor,
        instructor
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Instructor no encontrado o sin cambios"
        )

    return {"message": "Instructor actualizado correctamente"}

@router.get("/{id_instructor}/contactos")
def get_instructor_with_contactos(
    id_instructor: int,
    db: Session = Depends(get_db)
):
    data = instructor_crud.get_instructor_with_contactos(
        db,
        id_instructor
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Instructor no encontrado"
        )

    return data

@router.get("/supervisor/{id_supervisor}")
def get_instructores_por_supervisor(
    id_supervisor: int,
    db: Session = Depends(get_db)
):
    instructores = instructor_crud.get_instructores_by_supervisor(
        db,
        id_supervisor
    )

    if not instructores:
        raise HTTPException(
            status_code=404,
            detail="No hay instructores para este supervisor"
        )

    return instructores

def get_instructores_by_area(
    db: Session,
    id_area: int
):
    query = text("""
        SELECT 
            i.id_instructor,
            i.tipo_documento,
            i.numero_documento,
            i.nombres,
            i.apellidos,
            a.id_area,
            a.nombre_area,
            p.id_programa,
            p.nombre_programa
        FROM instructor i
        JOIN area_formacion a
            ON i.id_area = a.id_area
        JOIN programa p
            ON a.id_programa = p.id_programa
        WHERE a.id_area = :id_area
        ORDER BY i.nombres
    """)

    return db.execute(
        query,
        {"id_area": id_area}
    ).mappings().all()

@router.get("/area/{id_area}")
def get_instructores_por_area(
    id_area: int,
    db: Session = Depends(get_db)
):
    instructores = instructor_crud.get_instructores_by_area(
        db,
        id_area
    )

    if not instructores:
        raise HTTPException(
            status_code=404,
            detail="No hay instructores para esta área"
        )

    return instructores
