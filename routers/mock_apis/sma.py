"""Mock SMA Sunny Portal / Ennexos API endpoints."""
import random
import math
from datetime import datetime
from fastapi import APIRouter
from data.constants import PV_INSTALLATION

router = APIRouter(prefix="/mock/sma", tags=["Mock SMA"])


@router.get("/plants")
def list_plants():
    pv = PV_INSTALLATION
    return [{
        "plant_id": "sma-bel-kolea",
        "name": "Centrale PV Bel Kolea",
        "capacity_kwc": pv["capacity_kwc"],
        "panel_count": pv["panel_count"],
        "panel_type": pv["panel_type"],
        "inverter_count": 8,
        "status": "producing",
        "commissioning_date": "2023-06-15",
    }]


@router.get("/livedata/{plant_id}")
def get_livedata(plant_id: str):
    now = datetime.now()
    hour = now.hour + now.minute / 60
    month = now.month

    monthly_factors = {
        1: 0.45, 2: 0.53, 3: 0.80, 4: 0.95, 5: 1.12,
        6: 1.25, 7: 1.28, 8: 1.17, 9: 0.89, 10: 0.71,
        11: 0.45, 12: 0.40,
    }
    factor = monthly_factors.get(month, 0.8)

    sunrise, sunset = 6.5, 18.5
    if hour < sunrise or hour > sunset:
        power_kw = 0
        irradiance = 0
    else:
        solar_noon = (sunrise + sunset) / 2
        width = (sunset - sunrise) / 2
        normalized = (hour - solar_noon) / width
        bell = math.exp(-3 * normalized ** 2)
        power_kw = 500 * factor * bell + random.gauss(0, 8)
        power_kw = max(0, power_kw)
        irradiance = round(1000 * bell * factor, 0)

    daily_yield = power_kw * (hour - sunrise) / 2 if hour > sunrise else 0

    return {
        "plant_id": plant_id,
        "timestamp": now.isoformat(),
        "power_kw": round(power_kw, 1),
        "daily_yield_kwh": round(max(0, daily_yield), 1),
        "total_yield_mwh": round(PV_INSTALLATION["annual_production_mwh"] * 0.7, 1),
        "irradiance_wm2": round(max(0, irradiance)),
        "inverter_status": "ok",
        "inverters_online": 8,
        "inverters_total": 8,
    }


@router.get("/production/{plant_id}")
def get_production(plant_id: str, period: str = "day"):
    now = datetime.now()
    if period == "day":
        points = []
        for h in range(24):
            hour = h + 0.5
            sunrise, sunset = 6.5, 18.5
            if hour < sunrise or hour > sunset:
                kw = 0
            else:
                solar_noon = (sunrise + sunset) / 2
                width = (sunset - sunrise) / 2
                normalized = (hour - solar_noon) / width
                bell = math.exp(-3 * normalized ** 2)
                monthly_factors = {1: 0.45, 2: 0.53, 3: 0.80, 4: 0.95, 5: 1.12, 6: 1.25, 7: 1.28, 8: 1.17, 9: 0.89, 10: 0.71, 11: 0.45, 12: 0.40}
                kw = 500 * monthly_factors.get(now.month, 0.8) * bell
            points.append({"hour": h, "kw": round(max(0, kw + random.gauss(0, 5)), 1)})
        return {"period": "day", "date": now.strftime("%Y-%m-%d"), "data": points}

    from data.constants import MONTHLY_PV_VS_CONSUMPTION
    return {"period": period, "data": MONTHLY_PV_VS_CONSUMPTION}


@router.post("/auth")
def mock_auth(body: dict):
    return {"token": "mock-sma-jwt-2026", "status": "connected", "expires_in": 86400}
