from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from config import settings
from routers import dashboard, consumption, production, sites, reports, ai
from routers.mock_apis import comwatt, sma

app = FastAPI(
    title="NRGy by Alpha API",
    description="POC - Dashboard énergétique, monitoring solaire et génération de rapports IA",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(consumption.router)
app.include_router(production.router)
app.include_router(sites.router)
app.include_router(reports.router)
app.include_router(ai.router)
app.include_router(comwatt.router)
app.include_router(sma.router)


@app.get("/")
def root():
    return {
        "name": "NRGy by Alpha",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "dashboard": "/api/dashboard/{site_id}/overview",
            "consumption": "/api/consumption/{site_id}/load-curve",
            "production": "/api/production/{site_id}/monthly",
            "reports": "/api/reports/generate",
            "ai": "/api/ai/analyze",
            "sites": "/api/sites",
            "mock_comwatt": "/mock/comwatt/devices",
            "mock_sma": "/mock/sma/plants",
        },
    }
