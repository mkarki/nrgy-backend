import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from models.schemas import ReportRequest
from services.report_generator import generate_docx, generate_pptx, generate_xlsx

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.post("/generate")
async def generate_report(req: ReportRequest):
    if req.format == "docx":
        buffer = await generate_docx(req)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = f"Audit_Energetique_{req.site_id}.docx"
    elif req.format == "pptx":
        buffer = await generate_pptx(req)
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        filename = f"Rapport_Analyse_{req.site_id}.pptx"
    else:
        buffer = await generate_xlsx(req)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"Donnees_Energie_{req.site_id}.xlsx"

    return StreamingResponse(
        io.BytesIO(buffer),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
