from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import logging

from app.schemas.contrato import ContratoCreate, ContratoUpdate

logger = logging.getLogger(__name__)

# ==============================
# CREAR CONTRATO
# ==============================
def create_contrato(db: Session, contrato: ContratoCreate) -> bool:
    try:
        query = text("""
            INSERT INTO contrato (
                id_instructor,
                numero_contrato,
                fecha_inicio,
                fecha_fin,
                vigencia,
                valor_contrato,
                estado,
                cdp,
                crp,
                rubro,
                dependencia
            ) VALUES (
                :id_instructor,
                :numero_contrato,
                :fecha_inicio,
                :fecha_fin,
                :vigencia,
                :valor_contrato,
                :estado,
                :cdp,
                :crp,
                :rubro,
                :dependencia
            )
        """)

        db.execute(query, contrato.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear contrato: {e}")
        raise Exception("Error de base de datos al crear contrato")


# ==============================
# OBTENER POR ID
# ==============================
def get_contrato_by_id(db: Session, id_contrato: int):
    try:
        query = text("""
            SELECT *
            FROM contrato
            WHERE id_contrato = :id_contrato
        """)

        return db.execute(
            query,
            {"id_contrato": id_contrato}
        ).mappings().first()

    except Exception as e:
        logger.error(f"Error al obtener contrato: {e}")
        raise Exception("Error de base de datos")


# ==============================
# LISTAR TODOS
# ==============================
def get_all_contratos(db: Session):
    try:
        query = text("""
            SELECT *
            FROM contrato
        """)

        result = db.execute(query)
        return result.mappings().all()

    except Exception as e:
        logger.error(f"Error al listar contratos: {e}")
        raise Exception("Error de base de datos")


# ==============================
# LISTAR POR INSTRUCTOR
# ==============================
def get_contratos_by_instructor(db: Session, id_instructor: int):
    try:
        query = text("""
            SELECT *
            FROM contrato
            WHERE id_instructor = :id_instructor
        """)

        return db.execute(
            query,
            {"id_instructor": id_instructor}
        ).mappings().all()

    except Exception as e:
        logger.error(f"Error al listar contratos del instructor: {e}")
        raise Exception("Error de base de datos")


# ==============================
# ACTUALIZAR
# ==============================
def update_contrato(
    db: Session,
    id_contrato: int,
    contrato: ContratoUpdate
) -> bool:
    try:
        contrato_data = contrato.model_dump(exclude_unset=True)

        if not contrato_data:
            return False

        set_clause = ", ".join(
            [f"{key} = :{key}" for key in contrato_data.keys()]
        )

        query = text(f"""
            UPDATE contrato
            SET {set_clause}
            WHERE id_contrato = :id_contrato
        """)

        contrato_data["id_contrato"] = id_contrato

        result = db.execute(query, contrato_data)
        db.commit()

        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar contrato: {e}")
        raise Exception("Error de base de datos")


# ==============================
# ELIMINAR
# ==============================
def delete_contrato(db: Session, id_contrato: int) -> bool:
    try:
        query = text("""
            DELETE FROM contrato
            WHERE id_contrato = :id_contrato
        """)

        result = db.execute(
            query,
            {"id_contrato": id_contrato}
        )
        db.commit()

        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar contrato: {e}")
        raise Exception("Error de base de datos")

def get_contrato_informe(db: Session, id_contrato: int):
    query = text("""
        SELECT 
            co.id_contrato,
            co.numero_contrato,
            co.fecha_inicio,
            co.fecha_fin,
            co.vigencia,
            co.valor_contrato,
            co.estado,
            co.cdp,
            co.crp,
            co.rubro,
            co.dependencia,
            ins.nombres,
            ins.apellidos,
            ins.numero_documento
        FROM contrato co
        JOIN instructor ins 
            ON ins.id_instructor = co.id_instructor
        WHERE co.id_contrato = :id_contrato
    """)

    result = db.execute(
        query,
        {"id_contrato": id_contrato}
    ).mappings().first()

    return dict(result) if result else None

def get_contrato_instructor(db: Session):
    try:
        query = text("""
            SELECT 
            ins.nombres,
            ins.id_instructor,
            ins.apellidos,
            ins.numero_documento,
            co.numero_contrato,
            co.crp
            FROM instructor ins
            LEFT JOIN contrato co 
            ON co.id_instructor = ins.id_instructor;
        """)

        result = db.execute(query)
        return [dict(row) for row in result.mappings().all()]

    except Exception as e:
        logger.error(f"Error al listar contratos: {e}")
        raise Exception("Error de base de datos")