from pathlib import Path
from docxtpl import DocxTemplate
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session


from core.database import get_db
from app.crud.contrato import get_contrato_by_id
router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "templates" / "contrato_template.docx"

print(TEMPLATE_PATH)
print("EXISTE:", TEMPLATE_PATH.exists())

@router.get("/contrato/{id_contrato}")
def generar_informe_contrato(id_contrato: int, db: Session = Depends(get_db)):

    contrato = get_contrato_by_id(db, id_contrato)

    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")

    doc = DocxTemplate(str(TEMPLATE_PATH))

    contexto = {
        "nombres": contrato.numero_contrato,
        "documento": contrato.crp,
        "fecha_inicio": contrato.cdp,
        "fecha_fin": contrato.fecha_fin,
        "valor": contrato.valor_contrato
    }

    doc.render(contexto)

    output_path = BASE_DIR / "contrato_generado.docx"
    doc.save(output_path)

    return FileResponse(
        path=output_path,
        filename="contrato_generado.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )