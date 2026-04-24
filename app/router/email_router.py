from fastapi import APIRouter
from app.schemas.email_schema import EmailSchema
from app.services.email_service import enviar_correo

router = APIRouter(prefix="/email", tags=["Email"])


@router.post("/enviar")
async def enviar_email(data: EmailSchema):
    await enviar_correo(
        data.destinatario,
        data.asunto,
        data.contenido
    )
    return {"mensaje": "Correo enviado"}