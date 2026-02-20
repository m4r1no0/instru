from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from core.database import get_db
from app.router.dependencies import get_current_user
from app.schemas.instructor import InstructorCreate, InstructorUpdate
from app.crud.instructor import (
    create_instructor,
    get_user_by_id,
    get_user_by_email,
    get_instructor_with_contactos,
    get_instructores_by_supervisor,
    get_all_instructores_paginated,
    count_instructores,
    update_user_by_id
)

router = APIRouter()

# =====================================================
# CREAR INSTRUCTOR
# =====================================================

@router.post("/")
def crear_instructor(
    instructor: InstructorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    success = create_instructor(db, instructor)

    if not success:
        raise HTTPException(status_code=400, detail="No se pudo crear el instructor")

    return {"message": "Instructor creado correctamente"}

# =====================================================
# OBTENER INSTRUCTOR POR ID
# =====================================================

@router.get("/{id_instructor}")
def obtener_instructor(
    id_instructor: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    instructor = get_user_by_id(db, id_instructor)

    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")

    return instructor

# =====================================================
# OBTENER INSTRUCTOR POR EMAIL
# =====================================================

@router.get("/email/{email}")
def obtener_por_email(
    email: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    instructor = get_user_by_email(db, email)

    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")

    return instructor

# =====================================================
# OBTENER INSTRUCTOR CON CONTACTOS
# =====================================================

@router.get("/{id_instructor}/contactos")
def obtener_con_contactos(
    id_instructor: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    result = get_instructor_with_contactos(db, id_instructor)

    if not result:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")

    return result

# =====================================================
# OBTENER INSTRUCTORES POR SUPERVISOR
# =====================================================

@router.get("/supervisor/{id_supervisor}")
def listar_por_supervisor(
    id_supervisor: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_instructores_by_supervisor(db, id_supervisor)

# =====================================================
# LISTAR CON PAGINACIÓN
# =====================================================

@router.get("/")
def listar_instructores(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    data = get_all_instructores_paginated(db, page, size)
    total = count_instructores(db)

    return {
        "page": page,
        "size": size,
        "total": total,
        "total_pages": (total + size - 1) // size,
        "data": data
    }

# =====================================================
# ACTUALIZAR INSTRUCTOR
# =====================================================

@router.put("/{id_instructor}")
def actualizar_instructor(
    id_instructor: int,
    instructor: InstructorUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    updated = update_user_by_id(db, id_instructor, instructor)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Instructor no encontrado o sin cambios"
        )

    return {"message": "Instructor actualizado correctamente"}
