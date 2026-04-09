from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Query
from data.constants import CONSUMPTION_BREAKDOWN, DAY_NIGHT, TARIFFS, TGBTS
from data.mock_generator import generate_load_curve, generate_phase_data, generate_daily_summary
from models.schemas import LoadCurvePoint, DayNightSplit, TariffBreakdown, TGBT, DailySummary, PhasePoint

router = APIRouter(prefix="/api/consumption", tags=["Consumption"])


@router.get("/{site_id}/load-curve")
def get_load_curve(
    site_id: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    resolution: int = Query(15, description="Resolution in minutes"),
) -> List[LoadCurvePoint]:
    now = datetime.now()
    s = datetime.fromisoformat(start) if start else now - timedelta(days=1)
    e = datetime.fromisoformat(end) if end else now
    raw = generate_load_curve(site_id, s, e, resolution)
    return [LoadCurvePoint(**p) for p in raw]


@router.get("/{site_id}/day-night")
def get_day_night(site_id: str) -> DayNightSplit:
    dn = DAY_NIGHT
    total = CONSUMPTION_BREAKDOWN["total"]["mwh"]
    return DayNightSplit(
        day_pct=dn["day_pct"],
        night_pct=dn["night_pct"],
        day_mwh=round(total * dn["day_pct"] / 100, 1),
        night_mwh=round(total * dn["night_pct"] / 100, 1),
    )


@router.get("/{site_id}/tariff")
def get_tariff_breakdown(site_id: str) -> dict:
    cb = CONSUMPTION_BREAKDOWN
    periods_41 = TARIFFS["hta_41"]["periods"]
    breakdown = []
    for p in periods_41:
        key = p["name"].lower().replace("é", "e")
        if key == "pointe":
            data = cb["pointe"]
        elif key == "pleine":
            data = cb["pleine"]
        else:
            data = cb["creuse"]
        breakdown.append(TariffBreakdown(
            period=p["name"],
            hours=p["hours"],
            price_dzd_kwh=p["price_dzd_kwh"],
            consumption_mwh=data["mwh"],
            cost_dzd=data["cost_dzd"],
            color=p["color"],
        ))

    simulations = [
        {"name": "HTA 41", "price_label": "8,72 / 1,94 / 1,02", "annual_cost_dzd": 25_755_833, "current": True},
        {"name": "HTA 42", "price_label": "8,72 / 1,8", "annual_cost_dzd": 28_244_870, "current": False},
        {"name": "HTA 43", "price_label": "4,28 / 1,02", "annual_cost_dzd": 31_979_114, "current": False},
        {"name": "HTA 44", "price_label": "3,75", "annual_cost_dzd": 34_385_280, "current": False},
    ]

    return {"breakdown": breakdown, "simulations": simulations, "total_cost_dzd": cb["total"]["cost_dzd"]}


@router.get("/{site_id}/daily")
def get_daily_consumption(
    site_id: str,
    days: int = Query(30, description="Number of days"),
) -> List[DailySummary]:
    start = datetime.now() - timedelta(days=days)
    raw = generate_daily_summary(site_id, start, days)
    return [DailySummary(**d) for d in raw]


@router.get("/{site_id}/tgbt/{tgbt_id}")
def get_tgbt_detail(site_id: str, tgbt_id: str) -> dict:
    tgbts = TGBTS.get(site_id, [])
    tgbt_data = next((t for t in tgbts if t["id"] == tgbt_id), tgbts[0])
    tgbt = TGBT(**tgbt_data)

    now = datetime.now()
    phases = generate_phase_data(tgbt_id, now - timedelta(days=1), now, 15)

    return {
        "tgbt": tgbt,
        "phases": [PhasePoint(**p) for p in phases[:96]],  # limit to 24h at 15min
    }


@router.get("/{site_id}/tgbt")
def list_tgbts(site_id: str) -> List[TGBT]:
    tgbts = TGBTS.get(site_id, [])
    return [TGBT(**t) for t in tgbts]
