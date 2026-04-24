from pathlib import Path
import tempfile
import os 
from docxtpl import DocxTemplate
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session


from app.crud import contrato
from core.database import get_db

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "templates" / "contrato_template_acta.docx"

print(TEMPLATE_PATH)
print("EXISTE:", TEMPLATE_PATH.exists())

@router.get("/contratoDos/{id_contrato}")
def generar_informe_contrato(
    id_contrato: int,
    db: Session = Depends(get_db)
):

    data = contrato.get_contrato_informe(db, id_contrato)

    # 👇 PON EL PRINT AQUÍ
    print("DATA DEL INFORME:")
    print(data)

    if not data:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")

    template_path = os.path.join("app", "templates", "contrato_template_acta.docx")

    doc = DocxTemplate(template_path)

    doc.render(data)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp_file.name)

    return FileResponse(
        tmp_file.name,
        filename=f"Contrato_acta_{id_contrato}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )