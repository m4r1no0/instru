from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import logging

from app.schemas.users import UserCreate, UserUpdate
from core.security import get_hashed_password

logger = logging.getLogger(__name__)

# ===============================
# CREAR USUARIO
# ===============================
def create_user(db: Session, user: UserCreate) -> Optional[bool]:
    try:
        # Encriptar contraseña
        pass_encrypt = get_hashed_password(user.pass_hash)
        user.pass_hash = pass_encrypt

        query = text("""
            INSERT INTO usuarios (
                nombre,
                documento,
                id_rol,
                email,
                pass_hash,
                telefono,
                estado
            ) VALUES (
                :nombre,
                :documento,
                :id_rol,
                :email,
                :pass_hash,
                :telefono,
                :estado
            )
        """)

        db.execute(query, user.model_dump())
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al crear el usuario")


# ===============================
# LOGIN (CON HASH)
# ===============================
def get_user_by_email_for_login(db: Session, email: str):
    try:
        query = text("""
            SELECT 
                u.id_usuario,
                u.nombre,
                u.documento,
                u.id_rol,
                u.email,
                u.telefono,
                u.estado,
                r.nombre AS nombre_rol,
                u.pass_hash
            FROM usuarios u
            JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.email = :email
        """)

        result = db.execute(query, {"email": email}).mappings().first()
        return result

    except Exception as e:
        logger.error(f"Error al obtener usuario por email (login): {e}")
        raise Exception("Error de base de datos al obtener el usuario")


# ===============================
# OBTENER USUARIO POR EMAIL
# ===============================
def get_user_by_email(db: Session, email: str):
    try:
        query = text("""
            SELECT 
                u.id_usuario,
                u.nombre,
                u.documento,
                u.id_rol,
                u.email,
                u.telefono,
                u.estado,
                r.nombre AS nombre_rol
            FROM usuarios u
            JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.email = :email
        """)

        result = db.execute(query, {"email": email}).mappings().first()
        return result

    except Exception as e:
        logger.error(f"Error al obtener usuario por email: {e}")
        raise Exception("Error de base de datos al obtener el usuario")


# ===============================
# OBTENER USUARIO POR ID
# ===============================
def get_user_by_id(db: Session, user_id: int):
    try:
        query = text("""
            SELECT 
                u.id_usuario,
                u.nombre,
                u.documento,
                u.id_rol,
                u.email,
                u.telefono,
                u.estado,
                r.nombre AS nombre_rol
            FROM usuarios u
            JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = :id_usuario
        """)

        result = db.execute(query, {"id_usuario": user_id}).mappings().first()
        return result

    except Exception as e:
        logger.error(f"Error al obtener usuario por id: {e}")
        raise Exception("Error de base de datos al obtener el usuario")


# ===============================
# ACTUALIZAR USUARIO
# ===============================
def update_user_by_id(db: Session, user_id: int, user: UserUpdate) -> Optional[bool]:
    try:
        user_data = user.model_dump(exclude_unset=True)

        if not user_data:
            return False

        # Si se actualiza contraseña, volver a encriptar
        if "pass_hash" in user_data:
            user_data["pass_hash"] = get_hashed_password(user_data["pass_hash"])

        set_clauses = ", ".join([f"{key} = :{key}" for key in user_data.keys()])

        query = text(f"""
            UPDATE usuarios
            SET {set_clauses}
            WHERE id_usuario = :id_usuario
        """)

        user_data["id_usuario"] = user_id

        result = db.execute(query, user_data)
        db.commit()

        return result.rowcount > 0

    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")

# ===============================
# LISTAR TODOS LOS USUARIOS
# ===============================
def get_all_users(db: Session):
    try:
        query = text("""
            SELECT 
                u.id_usuario,
                u.nombre,
                u.documento,
                u.id_rol,
                u.email,
                u.telefono,
                u.estado,
                r.nombre AS nombre_rol
            FROM usuarios u
            JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY u.nombre ASC
        """)

        result = db.execute(query).mappings().all()
        return result

    except Exception as e:
        logger.error(f"Error al cargar usuarios: {e}")
        raise Exception("Error de base de datos usuarios")