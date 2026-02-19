from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import text

from core.database import get_db
from core.security import verify_token

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/access/login")


# ===================================
# OBTENER USUARIO ACTUAL DESDE TOKEN
# ===================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Verificar token y obtener ID
    user_id = verify_token(token)

    # Buscar usuario en base de datos
    query = """
        SELECT
            u.id_usuario,
            u.nombre,
            u.email,
            u.id_rol,
            r.nombre AS nombre_rol
        FROM usuarios u
        JOIN roles r ON u.id_rol = r.id_rol
        WHERE u.id_usuario = :user_id
    """

    result = db.execute(text(query), {"user_id": user_id})
    user = result.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return dict(user._mapping)


# ===================================
# DEPENDENCIA PARA ROLES
# ===================================

def require_role(role_name: str):
    def role_dependency(current_user: dict = Depends(get_current_user)):
        if current_user["nombre_rol"] != role_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )
        return current_user
    return role_dependency
