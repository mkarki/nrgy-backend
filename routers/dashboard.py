from typing import List, Optional
from fastapi import APIRouter
from data.constants import (
    SITES, CONSUMPTION_BREAKDOWN, PV_INSTALLATION, DAY_NIGHT, RECOMMENDATIONS,
)
from data.mock_generator import generate_alerts
from models.schemas import KPI, Alert

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/{site_id}/overview")
def get_overview(site_id: str) -> dict:
    site = SITES[site_id]
    pv = PV_INSTALLATION
    cb = CONSUMPTION_BREAKDOWN
    return {
        "site": site["name"],
        "kpis": [
            KPI(label="Consommation Annuelle", value=site["annual_consumption_mwh"], unit="MWh", delta_pct=-2.3, trend="down"),
            KPI(label="Production PV", value=pv["annual_production_mwh"], unit="MWh", delta_pct=5.1, trend="up"),
            KPI(label="CO2 Évité", value=pv["co2_avoided_tonnes_year"], unit="t/an", delta_pct=5.1, trend="up"),
            KPI(label="Économies", value=1_971_673, unit="DZD/an", delta_pct=3.8, trend="up"),
        ],
        "consumption_total_mwh": cb["total"]["mwh"],
        "consumption_cost_dzd": cb["total"]["cost_dzd"],
        "pv_coverage_pct": pv["coverage_rate_pct"],
        "day_night": DAY_NIGHT,
        "tgbt_distribution": [
            {"name": "TGBT 1", "share_pct": 40},
            {"name": "TGBT 2", "share_pct": 41},
            {"name": "TGBT 3", "share_pct": 19},
        ],
    }


@router.get("/{site_id}/kpis")
def get_kpis(site_id: str) -> List[KPI]:
    site = SITES[site_id]
    pv = PV_INSTALLATION
    return [
        KPI(label="Consommation Annuelle", value=site["annual_consumption_mwh"], unit="MWh", delta_pct=-2.3, trend="down"),
        KPI(label="Production PV", value=pv["annual_production_mwh"], unit="MWh", delta_pct=5.1, trend="up"),
        KPI(label="CO2 Évité", value=pv["co2_avoided_tonnes_year"], unit="t/an", delta_pct=5.1, trend="up"),
        KPI(label="Économies Annuelles", value=1_971_673, unit="DZD", delta_pct=3.8, trend="up"),
        KPI(label="Puissance Souscrite", value=site["subscribed_power_kw"], unit="kW"),
        KPI(label="Taux Couverture PV", value=pv["coverage_rate_pct"], unit="%", delta_pct=0, trend="stable"),
    ]


@router.get("/{site_id}/alerts")
def get_alerts(site_id: str) -> List[Alert]:
    raw = generate_alerts(site_id)
    return [Alert(**a) for a in raw]
