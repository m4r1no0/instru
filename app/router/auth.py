from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text

from core.security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from core.database import get_db  # Ajusta si tu conexión tiene otro nombre

router = APIRouter()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # ==============================
    # BUSCAR USUARIO POR EMAIL
    # ==============================
    query = """
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
    """

    result = db.execute(text(query), {"email": form_data.username})
    user = result.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales incorrectas"
        )

    # Convertir a diccionario
    user = dict(user._mapping)

    # ==============================
    # VERIFICAR CONTRASEÑA
    # ==============================
    if not verify_password(form_data.password, user["pass_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales incorrectas"
        )

    # ==============================
    # CREAR TOKEN
    # ==============================
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user["id_usuario"])},
        expires_delta=access_token_expires
    )

    # ==============================
    # RESPUESTA
    # ==============================
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id_usuario": user["id_usuario"],
            "nombre": user["nombre"],
            "email": user["email"],
            "rol": user["nombre_rol"]
        }
    }
