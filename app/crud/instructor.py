from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import logging

from app.schemas.instructor import InstructorCreate, InstructorUpdate
from core.security import get_hashed_password


logger = logging.getLogger(__name__)

def create_instructor(db: Session, user: InstructorCreate) -> Optional[bool]:
    try:
        print(user.pass_hash)
        pass_encrypt = get_hashed_password(user.pass_hash)
        print(pass_encrypt)
        user.pass_hash = pass_encrypt
        query = text("""
            INSERT INTO instructor (
                tipo_documento, numero_documento, nombres,
                apellido, fecha_nacimiento,
                fecha_expedicion, arl
            ) VALUES (
                :tipo_documento, :numero_documento, :nombres,
                :apellidos, :fecha_nacimiento,
                :fecha_expedicion, :arl
            )
        """)
        db.execute(query, user.model_dump())
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al crear el usuario")

def get_user_by_email_for_login(db: Session, email: str):
    try:
        query = text("""SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol,pass_hash
                     FROM usuarios
                     JOIN roles ON usuarios.id_rol = roles.id_rol
                     WHERE email = :email""")
        result = db.execute(query, {"email": email}).mappings().first()
        return result
    except Exception as e:
        logger.error(f"Error al obtener usuario por email: {e}")
        raise Exception("Error de base de datos al obtener el usuario estoy aqui")
    
def get_user_by_email(db: Session, email: str):
    try:
        query = text("""SELECT tipo_documento, nombres,apellidos,fecha_nacimiento, fecha_expedicion, id_supervisor,id_instructor arl FROM instructor
                     WHERE email = :email""")
        result = db.execute(query, {"email": email}).mappings().first()
        return result
    except Exception as e:
        logger.error(f"Error al obtener instructor por nombre: {e}")
        raise Exception("Error de base de datos al obtener el usuario estoy aqui")
    
def update_user_by_id(db: Session, user_id: int, user:InstructorUpdate) -> Optional[bool]:
    try:
        user_data= user.model_dump(exclude_unset=True)
        if not user_data:
            return False
        set_clauses = ",".join([f"{key} = :{key}" for key in user_data.keys()])
        sentencia = text (f""" UPDATE instructor
                          SET {set_clauses}   
                          WHERE id_instructor = :id_instructor """)

        user_data["id_instructor"] = user_id
        result = db.execute(sentencia,user_data)
        db.commit()
        return result.rowcount > 0
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear instructor: {e}")
        raise Exception("Error de base de datos al crear el instructor")
    
def get_user_by_id(db: Session, id: int):
    try:
        query = text("""
            SELECT id_instructor,tipo_documento, nombres,apellidos, numero_documento,fecha_nacimiento, fecha_expedicion,arl FROM instructor
            WHERE id_instructor = :id_instructor
        """)
        result = db.execute(query, {"id_instructor": id}).mappings().first()
        return result
    except Exception as e:
        logger.error(f"Error al obtener instructor por id: {e}")
        raise Exception("Error de base de datos al obtener el instructor")
    
def get_instructor_with_contactos(db: Session, id_instructor: int):
    try:
        query = text("""
            SELECT 
                i.id_instructor,
                i.tipo_documento,
                i.numero_documento,
                i.nombres,
                i.apellidos,
                i.fecha_nacimiento,
                i.fecha_expedicion,
                i.arl,
                c.id_contacto,
                c.correo_personal,
                c.correo_institucional,
                c.telefono
            FROM instructor i
            LEFT JOIN contacto c
                ON i.id_instructor = c.id_instructor
            WHERE i.id_instructor = :id_instructor
        """)

        return db.execute(
            query,
            {"id_instructor": id_instructor}
        ).mappings().all()

    except Exception as e:
        raise Exception("Error al obtener instructor con contactos")
    
def get_instructores_by_supervisor(
    db: Session,
    id_supervisor: int
):
    query = text("""
        SELECT 
            i.id_instructor,
            i.tipo_documento,
            i.numero_documento,
            i.nombres,
            i.apellidos,
            i.fecha_nacimiento,
            i.fecha_expedicion,
            i.id_supervisor,
            s.nombre AS nombre_supervisor
        FROM instructor i
        JOIN supervisor s
            ON i.id_supervisor = s.id_supervisor
        WHERE i.id_supervisor = :id_supervisor
        ORDER BY i.nombres
    """)

    return db.execute(
        query,
        {"id_supervisor": id_supervisor}
    ).mappings().all()
