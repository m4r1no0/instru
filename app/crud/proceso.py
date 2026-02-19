from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import logging

from app.schemas.proceso import ProcesoCreate, ProcesoUpdate

logger = logging.getLogger(__name__)


# =====================================
# CREAR
# =====================================
def create_proceso(db: Session, proceso: ProcesoCreate) -> bool:
    try:
        query = text("""
            INSERT INTO proceso (
                id_contrato,
                numero_proceso,
                informe_final,
                paz_y_salvo,
                link_secop
            ) VALUES (
                :id_contrato,
                :numero_proceso,
                :informe_final,
                :paz_y_salvo,
                :link_secop
            )
        """)

        db.execute(query, proceso.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear proceso: {e}")
        raise Exception("Error de base de datos")


# =====================================
# OBTENER POR ID
# =====================================
def get_proceso_by_id(db: Session, id_proceso: int):
    try:
        query = text("""
            SELECT *
            FROM proceso
            WHERE id_proceso = :id_proceso
        """)

        return db.execute(
            query,
            {"id_proceso": id_proceso}
        ).mappings().first()

    except Exception as e:
        raise Exception("Error de base de datos")


# =====================================
# LISTAR TODOS (con instructor)
# =====================================
def get_all_procesos(db: Session):
    try:
        query = text("""
            SELECT 
                p.id_proceso,
                p.id_contrato,
                c.id_instructor,
                p.numero_proceso,
                p.informe_final,
                p.paz_y_salvo,
                p.link_secop
            FROM proceso p
            JOIN contrato c
                ON p.id_contrato = c.id_contrato
        """)

        return db.execute(query).mappings().all()

    except Exception as e:
        raise Exception("Error de base de datos")


# =====================================
# LISTAR POR CONTRATO
# =====================================
def get_procesos_by_contrato(db: Session, id_contrato: int):
    try:
        query = text("""
            SELECT *
            FROM proceso
            WHERE id_contrato = :id_contrato
        """)

        return db.execute(
            query,
            {"id_contrato": id_contrato}
        ).mappings().all()

    except Exception as e:
        raise Exception("Error de base de datos")


# =====================================
# ACTUALIZAR
# =====================================
def update_proceso(
    db: Session,
    id_proceso: int,
    proceso: ProcesoUpdate
) -> bool:
    try:
        proceso_data = proceso.model_dump(exclude_unset=True)

        if not proceso_data:
            return False

        set_clause = ", ".join(
            [f"{key} = :{key}" for key in proceso_data.keys()]
        )

        query = text(f"""
            UPDATE proceso
            SET {set_clause}
            WHERE id_proceso = :id_proceso
        """)

        proceso_data["id_proceso"] = id_proceso

        result = db.execute(query, proceso_data)
        db.commit()

        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        raise Exception("Error de base de datos")


# =====================================
# ELIMINAR
# =====================================
def delete_proceso(db: Session, id_proceso: int) -> bool:
    try:
        query = text("""
            DELETE FROM proceso
            WHERE id_proceso = :id_proceso
        """)

        result = db.execute(
            query,
            {"id_proceso": id_proceso}
        )
        db.commit()

        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        raise Exception("Error de base de datos")
