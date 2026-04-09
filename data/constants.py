"""Real data from Bel Kolea energy audit - serves as seed for the entire POC."""

# === SITE INFO ===
SITES = {
    "bel-kolea": {
        "id": "bel-kolea",
        "name": "Usine Bel Algérie",
        "address": "Z.I. Mazafran Lot 2.18A BP 123, Kolea",
        "wilaya": "Tipaza",
        "activity": "Fabrication de produits laitiers",
        "phone": "+213 770 27 72 77",
        "website": "www.groupe-bel.com",
        "contract_type": "HTA 41",
        "subscribed_power_kw": 2000,
        "max_power_reached_kw": 1650,
        "annual_consumption_mwh": 6666,
        "climate_zone": "A",
        "avg_temp_c": 18.2,
    },
}

# === TGBT SPECIFICATIONS ===
TGBTS = {
    "bel-kolea": [
        {
            "id": "tgbt-1",
            "name": "TGBT 1",
            "description": "Ligne de production fromage portion + stockage",
            "s_moy_kva": 320,
            "s_median_kva": 354,
            "s_max_kva": 529,
            "s_min_kva": 146,
            "s_transfo_kva": 1250,
            "tc_pct": 26,
            "cos_phi": 0.96,
            "share_pct": 40,
            "has_onduleur": True,
            "onduleur_kva": 500,
            "weekend_consumption_pct": 21,
        },
        {
            "id": "tgbt-2",
            "name": "TGBT 2",
            "description": "Ligne de production + compresseurs + groupes froids",
            "s_moy_kva": 334,
            "s_median_kva": 360,
            "s_max_kva": 537,
            "s_min_kva": 61,
            "s_transfo_kva": 1000,
            "tc_pct": 33,
            "cos_phi": 0.93,
            "share_pct": 41,
            "has_onduleur": False,
            "onduleur_kva": 0,
            "weekend_consumption_pct": 24,
        },
        {
            "id": "tgbt-3",
            "name": "TGBT 3",
            "description": "Nouvelle ligne de production (à la demande)",
            "s_moy_kva": 156,
            "s_median_kva": 149,
            "s_max_kva": 422,
            "s_min_kva": 17,
            "s_transfo_kva": 1000,
            "tc_pct": 16,
            "cos_phi": 0.90,
            "share_pct": 19,
            "has_onduleur": False,
            "onduleur_kva": 0,
            "weekend_consumption_pct": 0,
        },
    ]
}

# === TARIFFS HTA 41 ===
TARIFFS = {
    "hta_41": {
        "name": "HTA 41",
        "periods": [
            {"name": "Pointe", "hours": "17:00-21:00", "start": 17, "end": 21, "price_dzd_kwh": 8.72, "color": "#ef4444"},
            {"name": "Pleine", "hours": "06:00-17:00 + 21:00-22:30", "start": 6, "end": 17, "price_dzd_kwh": 1.94, "color": "#f59e0b"},
            {"name": "Creuse", "hours": "22:30-06:00", "start": 22, "end": 6, "price_dzd_kwh": 1.02, "color": "#3b82f6"},
        ],
    },
    "hta_42": {"name": "HTA 42", "price_label": "8,72 / 1,8", "annual_cost_dzd": 28_244_870},
    "hta_43": {"name": "HTA 43", "price_label": "4,28 / 1,02", "annual_cost_dzd": 31_979_114},
    "hta_44": {"name": "HTA 44", "price_label": "3,75", "annual_cost_dzd": 34_385_280},
    "hta_41_total": {"name": "HTA 41", "price_label": "8,72 / 1,94 / 1,02", "annual_cost_dzd": 25_755_833},
}

# === CONSUMPTION BREAKDOWN (annual, source factures 2021) ===
CONSUMPTION_BREAKDOWN = {
    "creuse": {"mwh": 2060.8, "cost_dzd": 2_110_227},
    "pleine": {"mwh": 3474.1, "cost_dzd": 6_728_266},
    "pointe": {"mwh": 1131.2, "cost_dzd": 9_863_889},
    "total": {"mwh": 6666.0, "cost_dzd": 18_702_383},
}

# === DAY/NIGHT SPLIT ===
DAY_NIGHT = {
    "day_pct": 43,
    "night_pct": 57,
    "day_hours": "08:00-18:00",
    "night_hours": "18:00-08:00",
}

# === DAILY CONSUMPTION (recorded period 28/10 - 15/11/2022) ===
DAILY_CONSUMPTION = [
    {"date": "2022-10-28", "total_mwh": 11.73, "tgbt1": 4.27, "tgbt2": 4.93, "tgbt3": 2.53, "cold_group": 0.80, "temp_c": 22.5, "is_weekend": True},
    {"date": "2022-10-29", "total_mwh": 15.14, "tgbt1": 6.00, "tgbt2": 6.09, "tgbt3": 3.05, "cold_group": 1.00, "temp_c": 20.1, "is_weekend": True},
    {"date": "2022-10-30", "total_mwh": 22.35, "tgbt1": 9.10, "tgbt2": 8.04, "tgbt3": 5.21, "cold_group": 1.86, "temp_c": 19.8, "is_weekend": False},
    {"date": "2022-10-31", "total_mwh": 23.41, "tgbt1": 9.66, "tgbt2": 8.28, "tgbt3": 5.47, "cold_group": 1.93, "temp_c": 20.2, "is_weekend": False},
    {"date": "2022-11-01", "total_mwh": 23.02, "tgbt1": 9.44, "tgbt2": 8.14, "tgbt3": 5.44, "cold_group": 1.87, "temp_c": 18.5, "is_weekend": False},
    {"date": "2022-11-02", "total_mwh": 24.02, "tgbt1": 10.02, "tgbt2": 8.67, "tgbt3": 5.33, "cold_group": 1.95, "temp_c": 17.9, "is_weekend": False},
    {"date": "2022-11-03", "total_mwh": 16.77, "tgbt1": 6.71, "tgbt2": 6.80, "tgbt3": 3.26, "cold_group": 1.26, "temp_c": 17.2, "is_weekend": False},
    {"date": "2022-11-04", "total_mwh": 10.59, "tgbt1": 4.29, "tgbt2": 4.85, "tgbt3": 1.45, "cold_group": 0.74, "temp_c": 18.0, "is_weekend": True},
    {"date": "2022-11-05", "total_mwh": 13.71, "tgbt1": 5.55, "tgbt2": 6.43, "tgbt3": 1.73, "cold_group": 0.70, "temp_c": 16.5, "is_weekend": True},
    {"date": "2022-11-06", "total_mwh": 20.32, "tgbt1": 8.15, "tgbt2": 9.03, "tgbt3": 3.14, "cold_group": 1.05, "temp_c": 15.8, "is_weekend": False},
    {"date": "2022-11-07", "total_mwh": 20.46, "tgbt1": 8.16, "tgbt2": 8.89, "tgbt3": 3.41, "cold_group": 1.05, "temp_c": 16.2, "is_weekend": False},
    {"date": "2022-11-08", "total_mwh": 21.55, "tgbt1": 8.87, "tgbt2": 8.66, "tgbt3": 4.02, "cold_group": 1.59, "temp_c": 17.1, "is_weekend": False},
    {"date": "2022-11-09", "total_mwh": 21.34, "tgbt1": 8.84, "tgbt2": 8.33, "tgbt3": 4.17, "cold_group": 1.72, "temp_c": 18.4, "is_weekend": False},
    {"date": "2022-11-10", "total_mwh": 16.77, "tgbt1": 6.40, "tgbt2": 7.33, "tgbt3": 3.04, "cold_group": 1.22, "temp_c": 19.0, "is_weekend": False},
    {"date": "2022-11-11", "total_mwh": 10.17, "tgbt1": 3.77, "tgbt2": 5.20, "tgbt3": 1.20, "cold_group": 0.72, "temp_c": 19.5, "is_weekend": True},
    {"date": "2022-11-12", "total_mwh": 13.77, "tgbt1": 5.37, "tgbt2": 6.55, "tgbt3": 1.85, "cold_group": 1.05, "temp_c": 14.3, "is_weekend": True},
    {"date": "2022-11-13", "total_mwh": 19.89, "tgbt1": 8.21, "tgbt2": 8.36, "tgbt3": 3.32, "cold_group": 1.66, "temp_c": 15.1, "is_weekend": False},
    {"date": "2022-11-14", "total_mwh": 19.78, "tgbt1": 8.09, "tgbt2": 8.24, "tgbt3": 3.45, "cold_group": 1.57, "temp_c": 16.7, "is_weekend": False},
    {"date": "2022-11-15", "total_mwh": 19.69, "tgbt1": 8.20, "tgbt2": 8.39, "tgbt3": 3.10, "cold_group": 1.52, "temp_c": 17.3, "is_weekend": False},
]

# === PV INSTALLATION ===
PV_INSTALLATION = {
    "capacity_kwc": 632,
    "panel_count": 1160,
    "panel_type": "Jinko 545 Tiger Pro 72HC",
    "panel_power_wc": 545,
    "panel_efficiency_pct": 21.13,
    "annual_production_mwh": 828,
    "specific_yield_kwh_kwc": 1310,
    "coverage_rate_pct": 14,
    "co2_avoided_tonnes_year": 359,
    "investment_dzd": 79_500_000,
    "maintenance_dzd_year": 795_000,
    "roi_years": 15,
    "tri_pct": 3,
    "installation_type": "Toiture + structures acier galvanisé",
}

# === MONTHLY PV PRODUCTION VS CONSUMPTION ===
MONTHLY_PV_VS_CONSUMPTION = [
    {"month": "Janvier", "month_num": 1, "pv_mwh": 37, "consumption_mwh": 550},
    {"month": "Février", "month_num": 2, "pv_mwh": 44, "consumption_mwh": 521},
    {"month": "Mars", "month_num": 3, "pv_mwh": 66, "consumption_mwh": 570},
    {"month": "Avril", "month_num": 4, "pv_mwh": 79, "consumption_mwh": 565},
    {"month": "Mai", "month_num": 5, "pv_mwh": 93, "consumption_mwh": 459},
    {"month": "Juin", "month_num": 6, "pv_mwh": 104, "consumption_mwh": 454},
    {"month": "Juillet", "month_num": 7, "pv_mwh": 106, "consumption_mwh": 538},
    {"month": "Août", "month_num": 8, "pv_mwh": 97, "consumption_mwh": 538},
    {"month": "Septembre", "month_num": 9, "pv_mwh": 74, "consumption_mwh": 695},
    {"month": "Octobre", "month_num": 10, "pv_mwh": 59, "consumption_mwh": 647},
    {"month": "Novembre", "month_num": 11, "pv_mwh": 37, "consumption_mwh": 583},
    {"month": "Décembre", "month_num": 12, "pv_mwh": 33, "consumption_mwh": 545},
]

# === ECONOMICS PV ===
PV_ECONOMICS = {
    "pre_pv": {
        "creuse": {"mwh": 2060.8, "cost_dzd": 2_110_227},
        "pleine": {"mwh": 3474.1, "cost_dzd": 6_728_266},
        "pointe": {"mwh": 1131.2, "cost_dzd": 9_863_889},
        "total": {"mwh": 6666.0, "cost_dzd": 18_702_383},
    },
    "post_pv": {
        "creuse": {"mwh": 2060.8, "cost_dzd": 2_110_227},
        "pleine": {"mwh": 3474.1, "cost_dzd": 5_229_982},
        "pointe": {"mwh": 1131.2, "cost_dzd": 9_390_500},
        "total": {"mwh": 6666.0, "cost_dzd": 16_730_710},
    },
    "savings_dzd": 1_971_673,
}

# === CO2 PROJECTIONS ===
CO2_PROJECTIONS = [
    {"year": 1, "co2_tonnes": 359},
    {"year": 10, "co2_tonnes": 3590},
    {"year": 20, "co2_tonnes": 7180},
    {"year": 25, "co2_tonnes": 8975},
]

# === RECOMMENDATIONS ===
RECOMMENDATIONS = [
    {
        "id": "wash-d1",
        "category": "Horaires de lavage",
        "hypothesis": "D1",
        "description": "Déplacement lavage lundi de 23:30→04:00 vers 16:30→21:00",
        "energy_saving_mwh": 0,
        "investment_dzd": 0,
        "co2_avoided_tonnes": 0,
        "savings_dzd": 325_751,
    },
    {
        "id": "wash-d1s",
        "category": "Horaires de lavage",
        "hypothesis": "D1 + S",
        "description": "D1 + lavage simultané de toutes les lignes (pas de production heures de pointe)",
        "energy_saving_mwh": 132,
        "investment_dzd": 0,
        "co2_avoided_tonnes": 57,
        "savings_dzd": 1_195_005,
    },
    {
        "id": "wash-d2",
        "category": "Horaires de lavage",
        "hypothesis": "D2",
        "description": "Déplacement lavage jeudi de 09:00 vers mercredi 16:30→21:00",
        "energy_saving_mwh": 0,
        "investment_dzd": 0,
        "co2_avoided_tonnes": 0,
        "savings_dzd": 599_012,
    },
    {
        "id": "load-auto",
        "category": "Pilotage charges heures de pointe",
        "hypothesis": "Automatique",
        "description": "Pilotage automatique des charges non essentielles lors des heures de pointe",
        "energy_saving_mwh": 94,
        "investment_dzd": 700_000,
        "co2_avoided_tonnes": 41,
        "savings_dzd": 818_453,
    },
    {
        "id": "load-manual",
        "category": "Pilotage charges heures de pointe",
        "hypothesis": "Manuel",
        "description": "Pilotage manuel des charges non essentielles lors des heures de pointe",
        "energy_saving_mwh": 75,
        "investment_dzd": 0,
        "co2_avoided_tonnes": 33,
        "savings_dzd": 654_762,
    },
    {
        "id": "weekend-auto",
        "category": "Pilotage charges weekends",
        "hypothesis": "Automatique",
        "description": "Pilotage automatique des charges lors des weekends",
        "energy_saving_mwh": 19,
        "investment_dzd": 700_000,
        "co2_avoided_tonnes": 8,
        "savings_dzd": 52_232,
    },
    {
        "id": "cold-optim",
        "category": "Optimisation groupe froid",
        "hypothesis": "-",
        "description": "Optimisation de la consigne de température du groupe froid",
        "energy_saving_mwh": 33,
        "investment_dzd": 0,
        "co2_avoided_tonnes": 14,
        "savings_dzd": 91_405,
    },
]

# === ALERTS (based on real anomalies from the audit) ===
ALERT_TEMPLATES = [
    {"type": "voltage_drop", "severity": "warning", "tgbt": "tgbt-3", "message": "Chute de tension détectée sur TGBT 3 - {value}V pendant {duration}s"},
    {"type": "frequency_drop", "severity": "critical", "tgbt": "tgbt-3", "message": "Chute de fréquence sur TGBT 3 - coupure de {duration} min"},
    {"type": "overconsumption", "severity": "warning", "tgbt": None, "message": "Consommation weekend anormalement élevée: {value} kW (baseline attendu: 500 kW)"},
    {"type": "power_factor", "severity": "info", "tgbt": "tgbt-3", "message": "Facteur de puissance bas sur TGBT 3: cos φ = {value}"},
    {"type": "transformer_load", "severity": "info", "tgbt": "tgbt-1", "message": "Taux de charge transformateur TGBT 1 faible: {value}% - surdimensionné"},
]
