from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import logging

from app.schemas.pago import PagoCreate, PagoUpdate

logger = logging.getLogger(__name__)

# =====================================
# LISTAR TODOS LOS PAGOS
# =====================================
def get_all_pagos(db: Session) -> Optional[List[dict]]:
    """Lista todos los pagos con información del contrato e instructor"""
    try:
        query = text("""
            SELECT 
                p.id_pago,
                p.id_contrato,
                c.numero_contrato,
                CONCAT(i.nombres, ' ', i.apellidos) AS instructor_nombre,
                p.mes,
                p.valor_base,
                p.ajuste,
                p.valor_pagado,
                p.saldo
            FROM pago p
            INNER JOIN contrato c ON p.id_contrato = c.id_contrato
            INNER JOIN instructor i ON c.id_instructor = i.id_instructor
            ORDER BY  p.mes DESC
        """)

        result = db.execute(query).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error al listar pagos: {e}")
        raise Exception("Error de base de datos")

# =====================================
# LISTAR PAGOS POR CONTRATO
# =====================================
def get_pagos_by_contrato(db: Session, id_contrato: int) -> Optional[List[dict]]:
    """Lista todos los pagos de un contrato específico"""
    try:
        query = text("""
            SELECT 
                p.id_pago,
                p.id_contrato,
                c.numero_contrato,
                CONCAT(i.nombres, ' ', i.apellidos) AS instructor_nombre,
                p.mes,
                p.valor_base,
                p.ajuste,
                p.valor_pagado,
                p.saldo,
            FROM pago p
            LEFT JOIN contrato c ON p.id_contrato = c.id_contrato
            LEFT JOIN instructor i ON c.id_instructor = i.id_instructor
            WHERE p.id_contrato = :id_contrato
            ORDER BY p.mes DESC
        """)

        result = db.execute(query, {"id_contrato": id_contrato}).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error al listar pagos del contrato {id_contrato}: {e}")
        raise Exception("Error de base de datos")

# =====================================
# LISTAR PAGOS POR INSTRUCTOR
# =====================================
def get_pagos_by_instructor(db: Session, id_instructor: int) -> Optional[List[dict]]:
    """Lista todos los pagos de un instructor específico"""
    try:
        query = text("""
            SELECT 
                p.id_pago,
                p.id_contrato,
                c.numero_contrato,
                CONCAT(i.nombres, ' ', i.apellidos) AS instructor_nombre,
                p.mes,
                p.valor_base,
                p.ajuste,
                p.valor_pagado,
                p.saldo,
                p.created_at
            FROM pago p
            LEFT JOIN contrato c ON p.id_contrato = c.id_contrato
            LEFT JOIN instructor i ON c.id_instructor = i.id_instructor
            WHERE i.id_instructor = :id_instructor
            ORDER BY p.mes DESC
        """)

        result = db.execute(query, {"id_instructor": id_instructor}).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error al listar pagos del instructor {id_instructor}: {e}")
        raise Exception("Error de base de datos")

# =====================================
# CREAR PAGO (CON CÁLCULO AUTOMÁTICO DE SALDO)
# =====================================
def create_pago(db: Session, pago: PagoCreate) -> bool:
    try:
        # Calcular valor a pagar y saldo
        valor_a_pagar = pago.valor_base + (pago.ajuste or 0)
        saldo = valor_a_pagar - pago.valor_pagado
        
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

        params = {
            "id_contrato": pago.id_contrato,
            "mes": pago.mes,
            "valor_base": pago.valor_base,
            "ajuste": pago.ajuste or 0,
            "valor_pagado": pago.valor_pagado,
            "saldo": saldo
        }

        db.execute(query, params)
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear pago: {e}")
        raise Exception("Error de base de datos")

# =====================================
# OBTENER PAGO POR ID
# =====================================
def get_pago_by_id(db: Session, id_pago: int):
    try:
        query = text("""
            SELECT 
                p.*,
                c.numero_contrato,
                CONCAT(i.nombres, ' ', i.apellidos) AS instructor_nombre
            FROM pago p
            INNER JOIN contrato c ON p.id_contrato = c.id_contrato
            INNER JOIN instructor i ON c.id_instructor = i.id_instructor
            WHERE p.id_pago = :id_pago
        """)

        return db.execute(query, {"id_pago": id_pago}).mappings().first()

    except Exception as e:
        logger.error(f"Error al obtener pago {id_pago}: {e}")
        raise Exception("Error de base de datos")

# =====================================
# ACTUALIZAR PAGO (CON RECÁLCULO DE SALDO)
# =====================================
def update_pago(
    db: Session,
    id_pago: int,
    pago: PagoUpdate
) -> bool:
    try:
        # Obtener datos actuales
        pago_actual = get_pago_by_id(db, id_pago)
        if not pago_actual:
            return False
        
        # Preparar datos actualizados
        pago_data = pago.model_dump(exclude_unset=True)
        
        # Si se actualizan campos que afectan el saldo, recalcular
        if any(key in pago_data for key in ['valor_base', 'ajuste', 'valor_pagado']):
            valor_base = pago_data.get('valor_base', pago_actual['valor_base'])
            ajuste = pago_data.get('ajuste', pago_actual['ajuste'] or 0)
            valor_pagado = pago_data.get('valor_pagado', pago_actual['valor_pagado'])
            
            valor_a_pagar = valor_base + ajuste
            saldo = valor_a_pagar - valor_pagado
            pago_data['saldo'] = saldo

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
        logger.error(f"Error al actualizar pago {id_pago}: {e}")
        raise Exception("Error de base de datos")

# =====================================
# ELIMINAR PAGO
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
        logger.error(f"Error al eliminar pago {id_pago}: {e}")
        raise Exception("Error de base de datos")

# =====================================
# REPORTES
# =====================================
def get_resumen_pagos_por_instructor(db: Session) -> List[dict]:
    """Resumen de pagos agrupado por instructor"""
    try:
        query = text("""
            SELECT 
                i.id_instructor,
                CONCAT(i.nombres, ' ', i.apellidos) AS instructor_nombre,
                COUNT(DISTINCT c.id_contrato) AS total_contratos,
                COUNT(p.id_pago) AS total_pagos,
                SUM(p.valor_base) AS total_valor_base,
                SUM(p.ajuste) AS total_ajustes,
                SUM(p.valor_pagado) AS total_pagado,
                SUM(p.saldo) AS total_saldo
            FROM instructor i
            INNER JOIN contrato c ON i.id_instructor = c.id_instructor
            INNER JOIN pago p ON c.id_contrato = p.id_contrato
            GROUP BY i.id_instructor, i.nombres, i.apellidos
            ORDER BY total_saldo DESC
        """)

        result = db.execute(query).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error al obtener resumen por instructor: {e}")
        raise Exception("Error de base de datos")

def get_pagos_con_saldo_pendiente(db: Session) -> List[dict]:
    """Lista de pagos con saldo pendiente > 0"""
    try:
        query = text("""
            SELECT 
                p.id_pago,
                p.id_contrato,
                c.numero_contrato,
                CONCAT(i.nombres, ' ', i.apellidos) AS instructor_nombre,
                p.mes,
                p.valor_base,
                p.ajuste,
                p.valor_pagado,
                p.saldo
            FROM pago p
            INNER JOIN contrato c ON p.id_contrato = c.id_contrato
            INNER JOIN instructor i ON c.id_instructor = i.id_instructor
            WHERE p.saldo > 0
            ORDER BY p.saldo DESC
        """)

        result = db.execute(query).mappings().all()
        return result
    except Exception as e:
        logger.error(f"Error al listar pagos con saldo pendiente: {e}")
        raise Exception("Error de base de datos")