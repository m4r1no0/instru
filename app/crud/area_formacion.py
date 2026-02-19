from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.schemas.area_formacion import (
    AreaFormacionCreate,
    AreaFormacionUpdate
)

logger = logging.getLogger(__name__)


# =====================================
# CREAR
# =====================================
def create_area_formacion(
    db: Session,
    area: AreaFormacionCreate
) -> bool:
    try:
        query = text("""
            INSERT INTO area_formacion (
                id_programa,
                nombre_area,
                objeto,
                descripcion
            ) VALUES (
                :id_programa,
                :nombre_area,
                :objeto,
                :descripcion
            )
        """)

        db.execute(query, area.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear área: {e}")
        raise Exception("Error de base de datos")


# =====================================
# OBTENER POR ID
# =====================================
def get_area_by_id(
    db: Session,
    id_area: int
):
    query = text("""
        SELECT *
        FROM area_formacion
        WHERE id_area = :id_area
    """)

    return db.execute(
        query,
        {"id_area": id_area}
    ).mappings().first()


# =====================================
# LISTAR TODAS (CON PROGRAMA)
# =====================================
def get_all_areas(db: Session):
    query = text("""
        SELECT 
            a.id_area,
            a.id_programa,
            p.nombre_programa,
            a.nombre_area,
            a.objeto,
            a.descripcion
        FROM area_formacion a
        JOIN programa p
            ON a.id_programa = p.id_programa
        ORDER BY a.nombre_area
    """)

    return db.execute(query).mappings().all()


# =====================================
# LISTAR POR PROGRAMA
# =====================================
def get_areas_by_programa(
    db: Session,
    id_programa: int
):
    query = text("""
        SELECT *
        FROM area_formacion
        WHERE id_programa = :id_programa
        ORDER BY nombre_area
    """)

    return db.execute(
        query,
        {"id_programa": id_programa}
    ).mappings().all()


# =====================================
# ACTUALIZAR
# =====================================
def update_area_formacion(
    db: Session,
    id_area: int,
    area: AreaFormacionUpdate
) -> bool:

    area_data = area.model_dump(exclude_unset=True)

    if not area_data:
        return False

    set_clause = ", ".join(
        [f"{key} = :{key}" for key in area_data.keys()]
    )

    query = text(f"""
        UPDATE area_formacion
        SET {set_clause}
        WHERE id_area = :id_area
    """)

    area_data["id_area"] = id_area

    result = db.execute(query, area_data)
    db.commit()

    return result.rowcount > 0


# =====================================
# ELIMINAR
# =====================================
def delete_area_formacion(
    db: Session,
    id_area: int
) -> bool:

    query = text("""
        DELETE FROM area_formacion
        WHERE id_area = :id_area
    """)

    result = db.execute(
        query,
        {"id_area": id_area}
    )

    db.commit()

    return result.rowcount > 0
