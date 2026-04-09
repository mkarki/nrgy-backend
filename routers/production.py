from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter
from data.constants import MONTHLY_PV_VS_CONSUMPTION, PV_INSTALLATION, PV_ECONOMICS, CO2_PROJECTIONS
from data.mock_generator import generate_pv_daily_curve
from models.schemas import MonthlyPV, PVSummary

router = APIRouter(prefix="/api/production", tags=["Production"])


@router.get("/{site_id}/monthly")
def get_monthly_production(site_id: str) -> List[MonthlyPV]:
    return [MonthlyPV(**m) for m in MONTHLY_PV_VS_CONSUMPTION]


@router.get("/{site_id}/vs-consumption")
def get_pv_vs_consumption(site_id: str) -> dict:
    return {
        "monthly": MONTHLY_PV_VS_CONSUMPTION,
        "total_pv_mwh": PV_INSTALLATION["annual_production_mwh"],
        "total_consumption_mwh": 6666,
        "coverage_rate_pct": PV_INSTALLATION["coverage_rate_pct"],
    }


@router.get("/{site_id}/summary")
def get_pv_summary(site_id: str) -> PVSummary:
    pv = PV_INSTALLATION
    return PVSummary(
        capacity_kwc=pv["capacity_kwc"],
        panel_count=pv["panel_count"],
        annual_production_mwh=pv["annual_production_mwh"],
        coverage_rate_pct=pv["coverage_rate_pct"],
        co2_avoided_tonnes=pv["co2_avoided_tonnes_year"],
        investment_dzd=pv["investment_dzd"],
        roi_years=pv["roi_years"],
        savings_dzd=PV_ECONOMICS["savings_dzd"],
    )


@router.get("/{site_id}/daily-curve")
def get_daily_pv_curve(site_id: str, date: Optional[str] = None) -> List[dict]:
    dt = datetime.fromisoformat(date) if date else datetime.now()
    return generate_pv_daily_curve(dt)


@router.get("/{site_id}/economics")
def get_economics(site_id: str) -> dict:
    return {
        "pre_pv": PV_ECONOMICS["pre_pv"],
        "post_pv": PV_ECONOMICS["post_pv"],
        "annual_savings_dzd": PV_ECONOMICS["savings_dzd"],
        "investment_dzd": PV_INSTALLATION["investment_dzd"],
        "maintenance_dzd_year": PV_INSTALLATION["maintenance_dzd_year"],
        "roi_years": PV_INSTALLATION["roi_years"],
        "tri_pct": PV_INSTALLATION["tri_pct"],
        "co2_projections": CO2_PROJECTIONS,
    }
