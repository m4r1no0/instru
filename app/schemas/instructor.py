from datetime import date
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Instructor(BaseModel):
    id_instructor: int
    id_supervisor: int
    tipo_documento:str
    numero_documento:int
    nombres: str = Field(min_length=3, max_length=80)
    apellidos: str = Field(min_length=7, max_length=15)
    fecha_nacimiento:date
    fecha_expedicion:date
    arl:str

class InstructorCreate(Instructor):
    pass

class InstructorUpdate(Instructor):
    pass

class InstructorOut(Instructor):
    id_instructor:int
    nombre:str