from pydantic import BaseModel

class EmailSchema(BaseModel):
    destinatario: str
    asunto: str
    contenido: str