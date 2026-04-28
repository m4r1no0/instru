from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import logging

from app.schemas.contacto import ContactoCreate, ContactoUpdate

logger = logging.getLogger(__name__)

# =====================================
# LISTAR POR INSTRUCTOR
# =====================================
def get_all_contactos(db: Session) -> Optional[List[dict]]:
    try:
        query = text("""
            SELECT 
    c.id_instructor, 
    CONCAT(i.nombres, ' ', i.apellidos) AS nombre,
    c.id_contacto,
    c.telefono,
    c.correo_personal,
    c.correo_institucional
    FROM instructor i
    LEFT JOIN contacto c ON i.id_instructor = c.id_instructor
    WHERE i.id_instructor IN (
        SELECT id_instructor
        FROM contacto
        GROUP BY id_instructor
    )
    ORDER BY i.id_instructor;
        """)

        result = db.execute(
                query).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error al listar contactos: {e}")
        raise Exception("Error de base de datos")



# =====================================
# CREAR
# =====================================
def create_contacto(db: Session, contacto: ContactoCreate) -> bool:
    try:
        query = text("""
            INSERT INTO contacto (
                id_instructor,
                correo_personal,
                correo_institucional,
                telefono
            ) VALUES (
                :id_instructor,
                :correo_personal,
                :correo_institucional,
                :telefono
            )
        """)

        db.execute(query, contacto.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear contacto: {e}")
        raise Exception("Error de base de datos")


# =====================================
# OBTENER POR ID
# =====================================
def get_contacto_by_id(db: Session, id_contacto: int):
    try:
        query = text("""
            SELECT *
            FROM contacto
            WHERE id_contacto = :id_contacto
        """)

        return db.execute(
            query,
            {"id_contacto": id_contacto}
        ).mappings().first()

    except Exception as e:
        logger.error(f"Error al obtener contacto: {e}")
        raise Exception("Error de base de datos")


# =====================================
# ACTUALIZAR
# =====================================
def update_contacto(
    db: Session,
    id_contacto: int,
    contacto: ContactoUpdate
) -> bool:
    try:
        contacto_data = contacto.model_dump(exclude_unset=True)

        if not contacto_data:
            return False

        set_clause = ", ".join(
            [f"{key} = :{key}" for key in contacto_data.keys()]
        )

        query = text(f"""
            UPDATE contacto
            SET {set_clause}
            WHERE id_contacto = :id_contacto
        """)

        contacto_data["id_contacto"] = id_contacto

        result = db.execute(query, contacto_data)
        db.commit()

        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar contacto: {e}")
        raise Exception("Error de base de datos")


# =====================================
# ELIMINAR
# =====================================
def delete_contacto(db: Session, id_contacto: int) -> bool:
    try:
        query = text("""
            DELETE FROM contacto
            WHERE id_contacto = :id_contacto
        """)

        result = db.execute(
            query,
            {"id_contacto": id_contacto}
        )
        db.commit()

        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar contacto: {e}")
        raise Exception("Error de base de datos")
