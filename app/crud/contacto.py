from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import logging

from app.schemas.contacto import ContactoCreate, ContactoUpdate

logger = logging.getLogger(__name__)


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
# LISTAR POR INSTRUCTOR
# =====================================
def get_contactos_by_instructor(db: Session, id_instructor: int):
    try:
        query = text("""
            SELECT *
            FROM contacto
            WHERE id_instructor = :id_instructor
        """)

        return db.execute(
            query,
            {"id_instructor": id_instructor}
        ).mappings().all()

    except Exception as e:
        logger.error(f"Error al listar contactos: {e}")
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
