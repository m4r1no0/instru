from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.schemas.rol import RolCreate, RolUpdate

logger = logging.getLogger(__name__)


# =====================================
# CREAR
# =====================================
def create_rol(db: Session, rol: RolCreate) -> bool:
    try:
        query = text("""
            INSERT INTO rol (nombre, estado)
            VALUES (:nombre, :estado)
        """)

        db.execute(query, rol.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear rol: {e}")
        raise Exception("Error de base de datos")


# =====================================
# OBTENER POR ID
# =====================================
def get_rol_by_id(db: Session, id_rol: int):
    query = text("""
        SELECT *
        FROM rol
        WHERE id_rol = :id_rol
    """)

    return db.execute(
        query,
        {"id_rol": id_rol}
    ).mappings().first()


# =====================================
# LISTAR TODOS
# =====================================
def get_all_roles(db: Session):
    query = text("""
        SELECT *
        FROM rol
        ORDER BY nombre
    """)

    return db.execute(query).mappings().all()


# =====================================
# ACTUALIZAR
# =====================================
def update_rol(
    db: Session,
    id_rol: int,
    rol: RolUpdate
) -> bool:

    rol_data = rol.model_dump(exclude_unset=True)

    if not rol_data:
        return False

    set_clause = ", ".join(
        [f"{key} = :{key}" for key in rol_data.keys()]
    )

    query = text(f"""
        UPDATE rol
        SET {set_clause}
        WHERE id_rol = :id_rol
    """)

    rol_data["id_rol"] = id_rol

    result = db.execute(query, rol_data)
    db.commit()

    return result.rowcount > 0


# =====================================
# ELIMINAR
# =====================================
def delete_rol(db: Session, id_rol: int) -> bool:
    query = text("""
        DELETE FROM rol
        WHERE id_rol = :id_rol
    """)

    result = db.execute(
        query,
        {"id_rol": id_rol}
    )

    db.commit()

    return result.rowcount > 0
