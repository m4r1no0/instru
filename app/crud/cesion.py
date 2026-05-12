from sqlalchemy import text
from sqlalchemy.orm import Session
from app.schemas.cesion import CesionCreate


def create_cesion(db: Session, cesion: CesionCreate) -> bool:
    try:
        query = text("""
            INSERT INTO cesion (
                id_contrato,
                id_instructor,
                id_usuario,
                fecha_incio,
                fecha_cesion,
                fecha_modificacion
            ) VALUES (
                :id_contrato,
                :id_instructor,
                :id_usuario,
                :fecha_incio,
                :fecha_cesion,
                :fecha_modificacion
            )
        """)

        db.execute(query, cesion.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        print("Error:", e)
        return False


def get_all_cesiones(db: Session):
    query = text("""
        SELECT
            c.id_modificacion,
            c.id_contrato,
            co.numero_contrato,
            c.id_instructor,
            i.nombres AS instructor_nombres,
            i.apellidos AS instructor_apellidos,
            c.id_usuario,
            u.nombre AS usuario_nombre,
            c.fecha_incio,
            c.fecha_cesion,
            c.fecha_modificacion
        FROM cesion c
        JOIN instructor i ON c.id_instructor = i.id_instructor
        JOIN contrato co ON c.id_contrato = co.id_contrato
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        ORDER BY c.fecha_cesion DESC
    """)
    return db.execute(query).mappings().all()
    
