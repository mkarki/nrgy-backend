"""Mock Comwatt Energy API endpoints."""
import random
import math
from datetime import datetime
from fastapi import APIRouter

router = APIRouter(prefix="/mock/comwatt", tags=["Mock Comwatt"])


@router.get("/devices")
def list_devices():
    return [
        {"id": "cw-tgbt1", "name": "TGBT 1 - Production", "type": "energy_meter", "status": "online"},
        {"id": "cw-tgbt2", "name": "TGBT 2 - Compresseurs", "type": "energy_meter", "status": "online"},
        {"id": "cw-tgbt3", "name": "TGBT 3 - Nouvelle ligne", "type": "energy_meter", "status": "online"},
        {"id": "cw-cold", "name": "Groupe Froid Eau Glacée", "type": "energy_meter", "status": "online"},
    ]


@router.get("/realtime/{device_id}")
def get_realtime(device_id: str):
    now = datetime.now()
    hour = now.hour + now.minute / 60
    is_weekend = now.weekday() in (4, 5)

    base_kw = {"cw-tgbt1": 320, "cw-tgbt2": 334, "cw-tgbt3": 156, "cw-cold": 63}
    base = base_kw.get(device_id, 200)

    if is_weekend:
        factor = 0.4 + 0.05 * math.sin(hour * math.pi / 12)
    else:
        if 6 <= hour <= 17:
            factor = 0.85 + 0.15 * math.sin((hour - 6) * math.pi / 11)
        else:
            factor = 0.45

    kw = base * factor + random.gauss(0, base * 0.03)
    cos_phi = {"cw-tgbt1": 0.96, "cw-tgbt2": 0.93, "cw-tgbt3": 0.90, "cw-cold": 0.88}
    pf = cos_phi.get(device_id, 0.92)

    return {
        "device_id": device_id,
        "timestamp": now.isoformat(),
        "kw": round(max(0, kw), 1),
        "kva": round(max(0, kw / pf), 1),
        "power_factor": pf,
        "voltage": {
            "l1": round(230 + random.gauss(0, 1.5), 1),
            "l2": round(230 + random.gauss(0, 1.5), 1),
            "l3": round(230 + random.gauss(0, 1.5), 1),
        },
        "current": {
            "l1": round(max(0, kw / (230 * math.sqrt(3)) * 1000 + random.gauss(0, 2)), 1),
            "l2": round(max(0, kw / (230 * math.sqrt(3)) * 1000 + random.gauss(0, 2)), 1),
            "l3": round(max(0, kw / (230 * math.sqrt(3)) * 1000 + random.gauss(0, 2)), 1),
        },
    }


@router.post("/auth")
def mock_auth(body: dict):
    return {"token": "mock-comwatt-jwt-2026", "status": "connected", "expires_in": 86400}
