from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import logging

from app.schemas.users import UserCreate, UserUpdate
from core.security import get_hashed_password


logger = logging.getLogger(__name__)

def create_user(db: Session, user: UserCreate) -> Optional[bool]:
    try:
        print(user.pass_hash)
        pass_encrypt = get_hashed_password(user.pass_hash)
        print(pass_encrypt)
        user.pass_hash = pass_encrypt
        query = text("""
            INSERT INTO usuarios (
                id_finca,nombre, longitud,
                email, pass_hash,
                telefono, estado
            ) VALUES (
                :nombre, :documento, :id_rol,
                :email, :pass_hash,
                :telefono, :estado
            )
        """)
        db.execute(query, user.model_dump())
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al crear el usuario")