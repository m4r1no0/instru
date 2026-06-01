from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import logging

from app.schemas.direccion import DireccionCreate, DireccionUpdate

logger = logging.getLogger(__name__)


# ======================================
# CREAR
# ======================================
def create_direccion(db: Session, direccion: DireccionCreate) -> bool:
    try:
        query = text("""
            INSERT INTO direccion (
                id_instructor,
                municipio,
                complemento
            ) VALUES (
                :id_instructor,
                :municipio,
                :complemento
            )
        """)

        db.execute(query, direccion.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear dirección: {e}")
        raise Exception("Error de base de datos")


# ======================================
# OBTENER POR ID
# ======================================
def get_direccion_by_id(db: Session, id_direccion: int):
    try:
        query = text("""
            SELECT *
            FROM direccion
            WHERE id_direccion = :id_direccion
        """)

        return db.execute(
            query,
            {"id_direccion": id_direccion}
        ).mappings().first()

    except Exception as e:
        logger.error(f"Error al obtener dirección: {e}")
        raise Exception("Error de base de datos")


# ======================================
# LISTAR POR INSTRUCTOR
# ======================================
def get_direcciones_by_instructor(db: Session, id_instructor: int):
    try:
        query = text("""
            SELECT *
            FROM direccion
            WHERE id_instructor = :id_instructor
        """)

        return db.execute(
            query,
            {"id_instructor": id_instructor}
        ).mappings().all()

    except Exception as e:
        logger.error(f"Error al listar direcciones: {e}")
        raise Exception("Error de base de datos")


# ======================================
# ACTUALIZAR
# ======================================
def update_direccion(
    db: Session,
    id_direccion: int,
    direccion: DireccionUpdate
) -> bool:
    try:
        direccion_data = direccion.model_dump(exclude_unset=True)

        if not direccion_data:
            return False

        set_clause = ", ".join(
            [f"{key} = :{key}" for key in direccion_data.keys()]
        )

        query = text(f"""
            UPDATE direccion
            SET {set_clause}
            WHERE id_direccion = :id_direccion
        """)

        direccion_data["id_direccion"] = id_direccion

        result = db.execute(query, direccion_data)
        db.commit()

        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar dirección: {e}")
        raise Exception("Error de base de datos")


# ======================================
# ELIMINAR
# ======================================
def delete_direccion(db: Session, id_direccion: int) -> bool:
    try:
        query = text("""
            DELETE FROM direccion
            WHERE id_direccion = :id_direccion
        """)

        result = db.execute(
            query,
            {"id_direccion": id_direccion}
        )

        db.commit()
        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar dirección: {e}")
        raise Exception("Error de base de datos")

# ======================================
# OBTENER TODAS LAS DIRECCIONES
# ======================================
def get_all_direcciones(db: Session) -> Optional[List[dict]]:
    """
    Obtiene todas las direcciones usando SQL raw
    
    Returns:
        List[dict]: Lista de direcciones o None si hay error
    """
    try:
        query = text("""
            SELECT 
                i.id_instructor, 
                CONCAT(i.nombres, ' ', i.apellidos) AS nombre,
                d.id_direccion,
                d.municipio,
                d.complemento,
                c.telefono,
                c.correo_personal
            FROM instructor i
            LEFT JOIN direccion d ON i.id_instructor = d.id_instructor
            LEFT JOIN contacto c ON i.id_instructor = c.id_instructor
            WHERE i.id_instructor IN (
                SELECT id_instructor
                FROM direccion
                GROUP BY id_instructor
            )
            ORDER BY i.id_instructor, d.id_direccion;
        """)

        result = db.execute(query).mappings().all()
        
        # No hacer commit en SELECT
        # db.commit()  # ← ELIMINAR ESTO
        
        logger.info(f"Se encontraron {len(result)} direcciones")
        return result

    except Exception as e:
        # No hacer rollback en SELECT
        # db.rollback()  # ← ELIMINAR ESTO
        
        logger.error(f"Error al cargar direcciones: {e}")
        # Devolver lista vacía en lugar de lanzar excepción
        return []