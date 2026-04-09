"""Generates realistic time-series data seeded from Bel Kolea audit data."""

import math
import random
from datetime import datetime, timedelta
from .constants import TGBTS, DAILY_CONSUMPTION, MONTHLY_PV_VS_CONSUMPTION


def _is_weekend(dt: datetime) -> bool:
    return dt.weekday() in (4, 5)  # Friday-Saturday in Algeria


def _hour_profile_weekday() -> list[float]:
    """Hourly power factor for a typical weekday (0-23h). Peak ~800-1000kW."""
    return [
        0.45, 0.43, 0.42, 0.44, 0.55, 0.65,  # 00-05: night baseline
        0.72, 0.85, 0.92, 0.98, 1.00, 0.97,   # 06-11: ramp up to peak
        0.95, 0.98, 0.96, 0.94, 0.88, 0.80,   # 12-17: afternoon
        0.70, 0.62, 0.55, 0.50, 0.48, 0.46,   # 18-23: evening decline
    ]


def _hour_profile_weekend() -> list[float]:
    """Weekend profile: ~500kW baseline from cold groups."""
    return [0.38 + 0.04 * math.sin(h * math.pi / 12) for h in range(24)]


def _tgbt_share(tgbt_id: str) -> float:
    tgbts = TGBTS["bel-kolea"]
    for t in tgbts:
        if t["id"] == tgbt_id:
            return t["share_pct"] / 100
    return 0.33


def _pv_bell_curve(hour: float, month: int) -> float:
    """PV production bell curve based on solar position. Returns kW (0-500)."""
    monthly_factors = {
        1: 0.45, 2: 0.53, 3: 0.80, 4: 0.95, 5: 1.12,
        6: 1.25, 7: 1.28, 8: 1.17, 9: 0.89, 10: 0.71,
        11: 0.45, 12: 0.40,
    }
    factor = monthly_factors.get(month, 0.8)
    sunrise, sunset = 6.5, 18.5
    if hour < sunrise or hour > sunset:
        return 0.0
    solar_noon = (sunrise + sunset) / 2
    width = (sunset - sunrise) / 2
    normalized = (hour - solar_noon) / width
    bell = math.exp(-3 * normalized ** 2)
    peak_kw = 500 * factor
    return peak_kw * bell


def generate_load_curve(site_id: str, start: datetime, end: datetime, resolution_minutes: int = 15) -> list[dict]:
    """Generate load curve data points between start and end."""
    random.seed(42 + hash(start.isoformat()))
    points = []
    current = start
    base_kw = 800

    while current < end:
        is_wknd = _is_weekend(current)
        profile = _hour_profile_weekend() if is_wknd else _hour_profile_weekday()
        hour = current.hour + current.minute / 60
        hour_idx = min(int(hour), 23)
        factor = profile[hour_idx]

        if is_wknd:
            total_kw = 500 * factor + random.gauss(0, 15)
        else:
            total_kw = base_kw * factor + random.gauss(0, 25)

        total_kw = max(200, total_kw)

        tgbt1_kw = total_kw * 0.40 + random.gauss(0, 8)
        tgbt2_kw = total_kw * 0.41 + random.gauss(0, 8)
        tgbt3_kw = total_kw * 0.19 + random.gauss(0, 5)

        month = current.month
        pv_kw = _pv_bell_curve(hour, month) + random.gauss(0, 5)
        pv_kw = max(0, pv_kw)

        points.append({
            "timestamp": current.isoformat(),
            "total_kw": round(total_kw, 1),
            "tgbt1_kw": round(max(0, tgbt1_kw), 1),
            "tgbt2_kw": round(max(0, tgbt2_kw), 1),
            "tgbt3_kw": round(max(0, tgbt3_kw), 1),
            "pv_kw": round(pv_kw, 1),
            "net_kw": round(total_kw - pv_kw, 1),
        })
        current += timedelta(minutes=resolution_minutes)

    return points


def generate_phase_data(tgbt_id: str, start: datetime, end: datetime, resolution_minutes: int = 15) -> list[dict]:
    """Generate 3-phase voltage/current data for a TGBT."""
    random.seed(hash(tgbt_id) + hash(start.isoformat()))
    points = []
    current = start
    base_voltage = 230.0

    tgbts = TGBTS["bel-kolea"]
    tgbt = next((t for t in tgbts if t["id"] == tgbt_id), tgbts[0])
    base_current = tgbt["s_moy_kva"] / (base_voltage * math.sqrt(3)) * 1000

    while current < end:
        is_wknd = _is_weekend(current)
        profile = _hour_profile_weekend() if is_wknd else _hour_profile_weekday()
        hour_idx = min(current.hour, 23)
        factor = profile[hour_idx]

        v1 = base_voltage + random.gauss(0, 1.5)
        v2 = base_voltage + random.gauss(-0.5, 1.5)
        v3 = base_voltage + random.gauss(0.2, 1.5)

        # Simulate occasional voltage drops (like real data)
        if random.random() < 0.002 and tgbt_id == "tgbt-3":
            drop = random.uniform(10, 50)
            v1 -= drop
            v2 -= drop
            v3 -= drop

        i1 = base_current * factor + random.gauss(0, 3)
        i2 = base_current * factor + random.gauss(0, 3)
        i3 = base_current * factor + random.gauss(0, 3)

        kw = (v1 * i1 + v2 * i2 + v3 * i3) * tgbt["cos_phi"] / 1000

        points.append({
            "timestamp": current.isoformat(),
            "voltage_l1": round(v1, 1),
            "voltage_l2": round(v2, 1),
            "voltage_l3": round(v3, 1),
            "current_l1": round(max(0, i1), 2),
            "current_l2": round(max(0, i2), 2),
            "current_l3": round(max(0, i3), 2),
            "kw": round(max(0, kw), 1),
            "cos_phi": tgbt["cos_phi"],
        })
        current += timedelta(minutes=resolution_minutes)

    return points


def generate_daily_summary(site_id: str, start: datetime, days: int = 30) -> list[dict]:
    """Generate daily consumption summary based on real patterns."""
    random.seed(42)
    result = []
    real_data = DAILY_CONSUMPTION

    for d in range(days):
        dt = start + timedelta(days=d)
        is_wknd = _is_weekend(dt)
        seed_day = real_data[d % len(real_data)]

        jitter = random.gauss(1.0, 0.08)
        total = seed_day["total_mwh"] * jitter
        day_pct = 0.38 if is_wknd else 0.43

        result.append({
            "date": dt.strftime("%Y-%m-%d"),
            "total_mwh": round(total, 2),
            "day_mwh": round(total * day_pct, 2),
            "night_mwh": round(total * (1 - day_pct), 2),
            "tgbt1_mwh": round(total * 0.40, 2),
            "tgbt2_mwh": round(total * 0.41, 2),
            "tgbt3_mwh": round(total * 0.19, 2),
            "is_weekend": is_wknd,
            "temp_c": round(seed_day["temp_c"] + random.gauss(0, 1.5), 1),
        })

    return result


def generate_pv_daily_curve(date: datetime) -> list[dict]:
    """Generate PV production curve for a specific day."""
    month = date.month
    points = []
    for h in range(0, 24):
        for m in [0, 15, 30, 45]:
            hour = h + m / 60
            kw = _pv_bell_curve(hour, month) + random.gauss(0, 3)
            points.append({
                "timestamp": date.replace(hour=h, minute=m, second=0).isoformat(),
                "kw": round(max(0, kw), 1),
            })
    return points


def generate_alerts(site_id: str, count: int = 15) -> list[dict]:
    """Generate realistic alerts based on patterns from real audit."""
    random.seed(99)
    alerts = []
    now = datetime.now()

    alert_types = [
        ("voltage_drop", "warning", "tgbt-3", "Chute de tension TGBT 3: {v}V pendant {d}s"),
        ("frequency_drop", "critical", "tgbt-3", "Chute de fréquence TGBT 3: coupure de {d} min"),
        ("overconsumption", "warning", None, "Consommation weekend élevée: {v} kW"),
        ("power_factor", "info", "tgbt-3", "Cos φ bas TGBT 3: {v}"),
        ("transformer_load", "info", "tgbt-1", "Taux de charge faible TGBT 1: {v}%"),
    ]

    for i in range(count):
        alert_type, severity, tgbt, template = random.choice(alert_types)
        ts = now - timedelta(hours=random.randint(1, 720))
        msg = template.format(v=round(random.uniform(180, 225), 1), d=random.randint(5, 120))

        alerts.append({
            "id": f"alert-{i+1}",
            "type": alert_type,
            "severity": severity,
            "tgbt_id": tgbt,
            "message": msg,
            "timestamp": ts.isoformat(),
            "acknowledged": random.random() > 0.6,
        })

    return sorted(alerts, key=lambda x: x["timestamp"], reverse=True)
