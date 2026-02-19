from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.schemas.programa import ProgramaCreate, ProgramaUpdate

logger = logging.getLogger(__name__)


# =====================================
# CREAR
# =====================================
def create_programa(db: Session, programa: ProgramaCreate) -> bool:
    try:
        query = text("""
            INSERT INTO programa (
                codigo_programa,
                nombre_programa,
                nivel_formacion,
                modalidad
            ) VALUES (
                :codigo_programa,
                :nombre_programa,
                :nivel_formacion,
                :modalidad
            )
        """)

        db.execute(query, programa.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear programa: {e}")
        raise Exception("Error de base de datos")


# =====================================
# OBTENER POR ID
# =====================================
def get_programa_by_id(db: Session, id_programa: int):
    query = text("""
        SELECT *
        FROM programa
        WHERE id_programa = :id_programa
    """)

    return db.execute(
        query,
        {"id_programa": id_programa}
    ).mappings().first()


# =====================================
# OBTENER POR CODIGO
# =====================================
def get_programa_by_codigo(db: Session, codigo: str):
    query = text("""
        SELECT *
        FROM programa
        WHERE codigo_programa = :codigo
    """)

    return db.execute(
        query,
        {"codigo": codigo}
    ).mappings().first()


# =====================================
# LISTAR TODOS
# =====================================
def get_all_programas(db: Session):
    query = text("""
        SELECT *
        FROM programa
        ORDER BY nombre_programa
    """)

    return db.execute(query).mappings().all()


# =====================================
# ACTUALIZAR
# =====================================
def update_programa(
    db: Session,
    id_programa: int,
    programa: ProgramaUpdate
) -> bool:
    programa_data = programa.model_dump(exclude_unset=True)

    if not programa_data:
        return False

    set_clause = ", ".join(
        [f"{key} = :{key}" for key in programa_data.keys()]
    )

    query = text(f"""
        UPDATE programa
        SET {set_clause}
        WHERE id_programa = :id_programa
    """)

    programa_data["id_programa"] = id_programa

    result = db.execute(query, programa_data)
    db.commit()

    return result.rowcount > 0


# =====================================
# ELIMINAR
# =====================================
def delete_programa(db: Session, id_programa: int) -> bool:
    query = text("""
        DELETE FROM programa
        WHERE id_programa = :id_programa
    """)

    result = db.execute(
        query,
        {"id_programa": id_programa}
    )
    db.commit()

    return result.rowcount > 0
