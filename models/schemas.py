from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class TGBT(BaseModel):
    id: str
    name: str
    description: str
    s_moy_kva: float
    s_max_kva: float
    s_min_kva: float
    s_transfo_kva: float
    tc_pct: float
    cos_phi: float
    share_pct: float


class Site(BaseModel):
    id: str
    name: str
    address: str
    activity: str
    contract_type: str
    annual_consumption_mwh: float
    subscribed_power_kw: float
    tgbts: List[TGBT] = []


class KPI(BaseModel):
    label: str
    value: float
    unit: str
    delta_pct: Optional[float] = None
    trend: str = "stable"


class LoadCurvePoint(BaseModel):
    timestamp: str
    total_kw: float
    tgbt1_kw: float
    tgbt2_kw: float
    tgbt3_kw: float
    pv_kw: float
    net_kw: float


class DayNightSplit(BaseModel):
    day_pct: float
    night_pct: float
    day_mwh: float
    night_mwh: float


class TariffBreakdown(BaseModel):
    period: str
    hours: str
    price_dzd_kwh: float
    consumption_mwh: float
    cost_dzd: float
    color: str


class MonthlyPV(BaseModel):
    month: str
    month_num: int
    pv_mwh: float
    consumption_mwh: float


class PVSummary(BaseModel):
    capacity_kwc: float
    panel_count: int
    annual_production_mwh: float
    coverage_rate_pct: float
    co2_avoided_tonnes: float
    investment_dzd: float
    roi_years: int
    savings_dzd: float


class Alert(BaseModel):
    id: str
    type: str
    severity: str
    tgbt_id: Optional[str]
    message: str
    timestamp: str
    acknowledged: bool


class PhasePoint(BaseModel):
    timestamp: str
    voltage_l1: float
    voltage_l2: float
    voltage_l3: float
    current_l1: float
    current_l2: float
    current_l3: float
    kw: float
    cos_phi: float


class DailySummary(BaseModel):
    date: str
    total_mwh: float
    day_mwh: float
    night_mwh: float
    tgbt1_mwh: float
    tgbt2_mwh: float
    tgbt3_mwh: float
    is_weekend: bool
    temp_c: float


class ReportRequest(BaseModel):
    site_id: str = "bel-kolea"
    format: str = "docx"  # docx, pptx, xlsx
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    include_ai: bool = True


class AIAnalysisRequest(BaseModel):
    site_id: str = "bel-kolea"
    question: Optional[str] = None
    analysis_type: str = "summary"  # summary, consumption, recommendations, pv


class Recommendation(BaseModel):
    id: str
    category: str
    hypothesis: str
    description: str
    energy_saving_mwh: float
    investment_dzd: float
    co2_avoided_tonnes: float
    savings_dzd: float


class SourceConnection(BaseModel):
    platform: str  # comwatt, sma, papai
    email: str
    password: str


class SourceStatus(BaseModel):
    platform: str
    name: str
    connected: bool
    last_sync: Optional[str] = None
    devices_count: int = 0
