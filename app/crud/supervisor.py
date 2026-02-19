from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.schemas.supervisor import (
    SupervisorCreate,
    SupervisorUpdate
)

logger = logging.getLogger(__name__)


# =====================================
# CREAR
# =====================================
def create_supervisor(
    db: Session,
    supervisor: SupervisorCreate
) -> bool:
    try:
        query = text("""
            INSERT INTO supervisor (nombre)
            VALUES (:nombre)
        """)

        db.execute(query, supervisor.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear supervisor: {e}")
        raise Exception("Error de base de datos")


# =====================================
# OBTENER POR ID
# =====================================
def get_supervisor_by_id(
    db: Session,
    id_supervisor: int
):
    query = text("""
        SELECT *
        FROM supervisor
        WHERE id_supervisor = :id_supervisor
    """)

    return db.execute(
        query,
        {"id_supervisor": id_supervisor}
    ).mappings().first()


# =====================================
# LISTAR TODOS
# =====================================
def get_all_supervisores(db: Session):
    query = text("""
        SELECT *
        FROM supervisor
        ORDER BY nombre
    """)

    return db.execute(query).mappings().all()


# =====================================
# ACTUALIZAR
# =====================================
def update_supervisor(
    db: Session,
    id_supervisor: int,
    supervisor: SupervisorUpdate
) -> bool:

    supervisor_data = supervisor.model_dump(
        exclude_unset=True
    )

    if not supervisor_data:
        return False

    set_clause = ", ".join(
        [f"{key} = :{key}" for key in supervisor_data.keys()]
    )

    query = text(f"""
        UPDATE supervisor
        SET {set_clause}
        WHERE id_supervisor = :id_supervisor
    """)

    supervisor_data["id_supervisor"] = id_supervisor

    result = db.execute(query, supervisor_data)
    db.commit()

    return result.rowcount > 0


# =====================================
# ELIMINAR
# =====================================
def delete_supervisor(
    db: Session,
    id_supervisor: int
) -> bool:

    query = text("""
        DELETE FROM supervisor
        WHERE id_supervisor = :id_supervisor
    """)

    result = db.execute(
        query,
        {"id_supervisor": id_supervisor}
    )

    db.commit()

    return result.rowcount > 0
