from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import logging

from app.schemas.instructor import InstructorCreate, InstructorUpdate
from core.security import get_hashed_password


logger = logging.getLogger(__name__)

def create_instructor(db: Session, instructor: InstructorCreate):
    try:
        query = text("""
            INSERT INTO instructor (
                tipo_documento, numero_documento, nombres,
                apellidos, fecha_nacimiento,
                fecha_expedicion, arl, id_supervisor
            ) VALUES (
                :tipo_documento, :numero_documento, :nombres,
                :apellidos, :fecha_nacimiento,
                :fecha_expedicion, :arl, :id_supervisor
            )
        """)

        db.execute(query, instructor.model_dump())
        db.commit()

        return {"message": "Instructor creado correctamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

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
    
def update_user_by_id(db: Session, user_id: int, user: InstructorUpdate) -> Optional[bool]:
    try:
        # Excluir campos no enviados (solo actualizar los que vienen en la petición)
        user_data = user.model_dump(exclude_unset=True)
        
        # Si no hay datos para actualizar, retornar False
        if not user_data:
            return False
        
        # Construir dinámicamente la parte SET de la consulta SQL
        # Ejemplo: "nombre = :nombre, email = :email"
        set_clauses = ", ".join([f"{key} = :{key}" for key in user_data.keys()])
        
        # Crear la consulta SQL con text()
        sentencia = text(f"""
            UPDATE instructor 
            SET {set_clauses}   
            WHERE id_instructor = :id_instructor
        """)
        
        # Agregar el id_instructor al diccionario de parámetros
        user_data["id_instructor"] = user_id
        
        # Ejecutar la consulta
        result = db.execute(sentencia, user_data)
        
        # Confirmar los cambios en la base de datos
        db.commit()
        
        # Retornar True si se actualizó al menos una fila, False si no
        return result.rowcount > 0
        
    except Exception as e:
        # Revertir cualquier cambio pendiente
        db.rollback()
        # Registrar el error real para debugging
        print(f"ERROR REAL: {e}")
        # Lanzar una excepción con mensaje claro
        raise Exception(f"Error de base de datos al actualizar el usuario con ID {user_id}: {str(e)}")
    
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

def get_all_instructores_paginated(
    db: Session,
    page: int = 1,
    size: int = 10
):
    try:
        offset = (page - 1) * size

        query = text("""SELECT 
                            s.id_supervisor,
                            s.nombre,
                            c.numero_contrato,
                            c.crp,
                            c.cdp,
                            c.estado,
                            c.valor_contrato,
                            c.valor_mes,
                            c.valorAdDi,
                            c.rubro,
                            c.dependencia,
                            c.fecha_inicio,
                            c.fecha_fin,
                            pro.nombre_programa,
                            CONCAT(i.nombres, ' ', i.apellidos) AS instructor_nombre,
                            i.tipo_documento,
                            i.id_instructor,
                            i.estado AS estado_instructor,
                            i.fecha_nacimiento,
                            i.fecha_expedicion,
                            i.numero_documento,
                            a.nombre_area
                        FROM instructor i
                        LEFT JOIN supervisor s 
                            ON s.id_supervisor = i.id_supervisor
                        LEFT JOIN contrato c 
                            ON i.id_instructor = c.id_instructor
                        LEFT JOIN instructor_programa ins 
                            ON i.id_instructor = ins.id_instructor
                        LEFT JOIN programa_formacion pro 
                            ON pro.id_programa = ins.id_programa
                        LEFT JOIN area_formacion a 
                            ON i.id_area = a.id_area
            LIMIT :limit OFFSET :offset
        """)

        result = db.execute(
            query,
            {
                "limit": size,
                "offset": offset
            }
        ).mappings().all()
        return result

    except Exception as e:
        logger.error(f"Error al obtener instructores paginados: {e}")
        raise Exception("Error de base de datos al obtener instructores")

def count_instructores(db: Session):
    query = text("SELECT COUNT(*) as total FROM instructor")
    result = db.execute(query).mappings().first()
    return result["total"]


