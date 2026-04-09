from fastapi import APIRouter
from models.schemas import AIAnalysisRequest
from services.ai_service import (
    generate_executive_summary,
    generate_consumption_analysis,
    generate_recommendations,
    generate_pv_assessment,
    generate_chat_response,
)
from data.constants import SITES, TGBTS, PV_INSTALLATION

router = APIRouter(prefix="/api/ai", tags=["AI Analysis"])


@router.post("/analyze")
def analyze(req: AIAnalysisRequest) -> dict:
    site = SITES.get(req.site_id, SITES["bel-kolea"])
    tgbts = TGBTS.get(req.site_id, TGBTS["bel-kolea"])

    if req.analysis_type == "summary":
        content = generate_executive_summary(site)
    elif req.analysis_type == "consumption":
        content = generate_consumption_analysis(tgbts)
    elif req.analysis_type == "recommendations":
        content = generate_recommendations(site)
    elif req.analysis_type == "pv":
        content = generate_pv_assessment(PV_INSTALLATION)
    else:
        content = generate_executive_summary(site)

    return {"analysis_type": req.analysis_type, "content": content}


@router.post("/chat")
def chat(req: AIAnalysisRequest) -> dict:
    site = SITES.get(req.site_id, SITES["bel-kolea"])
    question = req.question or "Fais un résumé de la situation énergétique du site."
    content = generate_chat_response(question, site)
    return {"question": question, "response": content}


@router.post("/recommend")
def recommend(req: AIAnalysisRequest) -> dict:
    site = SITES.get(req.site_id, SITES["bel-kolea"])
    content = generate_recommendations(site)
    return {"recommendations": content}
