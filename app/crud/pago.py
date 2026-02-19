from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import logging

from app.schemas.pago import PagoCreate, PagoUpdate

logger = logging.getLogger(__name__)


# =====================================
# CREAR
# =====================================
def create_pago(db: Session, pago: PagoCreate) -> bool:
    try:
        query = text("""
            INSERT INTO pago (
                id_contrato,
                mes,
                valor_base,
                ajuste,
                valor_pagado,
                saldo
            ) VALUES (
                :id_contrato,
                :mes,
                :valor_base,
                :ajuste,
                :valor_pagado,
                :saldo
            )
        """)

        db.execute(query, pago.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear pago: {e}")
        raise Exception("Error de base de datos")


# =====================================
# OBTENER POR ID (CON JOIN)
# =====================================
def get_pago_by_id(db: Session, id_pago: int):
    try:
        query = text("""
            SELECT 
                p.*,
                c.id_instructor
            FROM pago p
            JOIN contrato c 
                ON p.id_contrato = c.id_contrato
            WHERE p.id_pago = :id_pago
        """)

        return db.execute(
            query,
            {"id_pago": id_pago}
        ).mappings().first()

    except Exception as e:
        logger.error(f"Error al obtener pago: {e}")
        raise Exception("Error de base de datos")


# =====================================
# LISTAR TODOS (CON JOIN)
# =====================================
def get_all_pagos(db: Session):
    try:
        query = text("""
            SELECT 
                p.*,
                c.id_instructor
            FROM pago p
            JOIN contrato c 
                ON p.id_contrato = c.id_contrato
            ORDER BY p.id_pago DESC
        """)

        return db.execute(query).mappings().all()

    except Exception as e:
        logger.error(f"Error al listar pagos: {e}")
        raise Exception("Error de base de datos")


# =====================================
# LISTAR POR CONTRATO
# =====================================
def get_pagos_by_contrato(db: Session, id_contrato: int):
    try:
        query = text("""
            SELECT 
                p.*,
                c.id_instructor
            FROM pago p
            JOIN contrato c 
                ON p.id_contrato = c.id_contrato
            WHERE p.id_contrato = :id_contrato
        """)

        return db.execute(
            query,
            {"id_contrato": id_contrato}
        ).mappings().all()

    except Exception as e:
        logger.error(f"Error al listar pagos por contrato: {e}")
        raise Exception("Error de base de datos")


# =====================================
# ACTUALIZAR
# =====================================
def update_pago(db: Session, id_pago: int, pago: PagoUpdate) -> bool:
    try:
        pago_data = pago.model_dump(exclude_unset=True)

        if not pago_data:
            return False

        set_clause = ", ".join(
            [f"{key} = :{key}" for key in pago_data.keys()]
        )

        query = text(f"""
            UPDATE pago
            SET {set_clause}
            WHERE id_pago = :id_pago
        """)

        pago_data["id_pago"] = id_pago

        result = db.execute(query, pago_data)
        db.commit()

        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar pago: {e}")
        raise Exception("Error de base de datos")


# =====================================
# ELIMINAR
# =====================================
def delete_pago(db: Session, id_pago: int) -> bool:
    try:
        query = text("""
            DELETE FROM pago
            WHERE id_pago = :id_pago
        """)

        result = db.execute(query, {"id_pago": id_pago})
        db.commit()

        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar pago: {e}")
        raise Exception("Error de base de datos")
