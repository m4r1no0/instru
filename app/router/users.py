from typing import List
from fastapi import APIRouter, Depends, HTTPException, logger, status
from sqlalchemy.orm import Session
from core.database import get_db
from app.schemas.users import UserCreate, UserUpdate,UserOut
from app.router.dependencies import get_current_user
from app.crud import users as crud_users

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate,
                db: Session = Depends(get_db),
                user_token: UserOut = Depends(get_current_user)
):
    try:
        crud_users.create_user(db, user)
        return {"message": "Usuario creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/by-email")
def get_user(email: str, db: Session = Depends(get_db),
             user_token: UserOut = Depends(get_current_user)):
    try:
        user = crud_users.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db),
                user_token: UserOut = Depends(get_current_user)):
    try:
        success = crud_users.update_user_by_id(db, user_id, user)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")
        return {"message": "Usuario actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# ===============================
# LISTAR TODOS LOS USUARIOS
# ===============================
@router.get("/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return crud_users.get_all_users(db)
