from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
import logging

from app.schemas.poliza import PolizaCreate, PolizaUpdate

logger = logging.getLogger(__name__)


# =====================================
# VALIDAR ESTADO AUTOMATICO
# =====================================
def calcular_estado(fecha_fin):
    if fecha_fin and fecha_fin < date.today():
        return "VENCIDA"
    return "ACTIVA"


# =====================================
# VALIDAR NUMERO UNICO
# =====================================
def get_poliza_by_numero(db: Session, numero: str):
    query = text("""
        SELECT *
        FROM poliza
        WHERE numero_poliza = :numero
    """)
    return db.execute(
        query,
        {"numero": numero}
    ).mappings().first()


# =====================================
# CREAR
# =====================================
def create_poliza(db: Session, poliza: PolizaCreate) -> bool:
    try:
        estado = calcular_estado(poliza.fecha_fin)

        query = text("""
            INSERT INTO poliza (
                id_instructor,
                numero_poliza,
                tipo_poliza,
                aseguradora,
                fecha_inicio,
                fecha_fin,
                valor_asegurado,
                estado,
                documento_pdf,
                observaciones
            ) VALUES (
                :id_instructor,
                :numero_poliza,
                :tipo_poliza,
                :aseguradora,
                :fecha_inicio,
                :fecha_fin,
                :valor_asegurado,
                :estado,
                :documento_pdf,
                :observaciones
            )
        """)

        data = poliza.model_dump()
        data["estado"] = estado

        db.execute(query, data)
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear póliza: {e}")
        raise Exception("Error de base de datos")


# =====================================
# LISTAR TODAS CON INSTRUCTOR
# =====================================
def get_all_polizas(db: Session):
    query = text("""
        SELECT 
            p.id_poliza,
            p.numero_poliza,
            p.tipo_poliza,
            p.aseguradora,
            p.fecha_inicio,
            p.fecha_fin,
            p.valor_asegurado,
            p.estado,
            i.nombres,
            i.apellidos
        FROM poliza p
        JOIN instructor i
            ON p.id_instructor = i.id_instructor
        ORDER BY p.fecha_inicio DESC
    """)

    return db.execute(query).mappings().all()


# =====================================
# LISTAR POR INSTRUCTOR
# =====================================
def get_polizas_by_instructor(db: Session, id_instructor: int):
    query = text("""
        SELECT *
        FROM poliza
        WHERE id_instructor = :id_instructor
        ORDER BY fecha_inicio DESC
    """)

    return db.execute(
        query,
        {"id_instructor": id_instructor}
    ).mappings().all()


# =====================================
# ACTUALIZAR
# =====================================
def update_poliza(
    db: Session,
    id_poliza: int,
    poliza: PolizaUpdate
) -> bool:

    poliza_data = poliza.model_dump(exclude_unset=True)

    if not poliza_data:
        return False

    if "fecha_fin" in poliza_data:
        poliza_data["estado"] = calcular_estado(
            poliza_data["fecha_fin"]
        )

    set_clause = ", ".join(
        [f"{key} = :{key}" for key in poliza_data.keys()]
    )

    query = text(f"""
        UPDATE poliza
        SET {set_clause}
        WHERE id_poliza = :id_poliza
    """)

    poliza_data["id_poliza"] = id_poliza

    result = db.execute(query, poliza_data)
    db.commit()

    return result.rowcount > 0


# =====================================
# ELIMINAR
# =====================================
def delete_poliza(db: Session, id_poliza: int) -> bool:
    query = text("""
        DELETE FROM poliza
        WHERE id_poliza = :id_poliza
    """)

    result = db.execute(
        query,
        {"id_poliza": id_poliza}
    )

    db.commit()

    return result.rowcount > 0
