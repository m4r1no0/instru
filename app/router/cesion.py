from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from app.schemas.cesion import (
    CesionCreate,
    CesionUpdate,
    CesionOut,
    CesionWithRelations,
)
from app.crud import cesion as cesion_crud

router = APIRouter()


@router.post("/create")
def create_cesion(cesion_data: CesionCreate, db: Session = Depends(get_db)):
    created = cesion_crud.create_cesion(db, cesion_data)

    if not created:
        raise HTTPException(status_code=400, detail="No se pudo crear la cesion")

    return {"message": "Cesion creada correctamente"}


@router.get("/", response_model=List[CesionWithRelations])
def get_all_cesiones(db: Session = Depends(get_db)):
    return cesion_crud.get_all_cesiones(db)
