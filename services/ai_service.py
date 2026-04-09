"""AI-powered analysis and report generation using OpenAI GPT-4o-mini."""

from openai import OpenAI
from config import settings

SYSTEM_PROMPT = """Tu es un ingénieur énergie expert utilisant Sungy, un intégrateur de solutions solaires en Algérie.
Tu analyses les données électriques de sites industriels et rédiges des rapports d'audit énergétique professionnels.
Tu utilises les unités : kWh, MWh, kW, kVA, DZD (Dinar Algérien), tonnes CO2.
Ton ton est professionnel, précis et orienté vers des recommandations actionnables.
Tu structures tes analyses avec des constats chiffrés et des recommandations concrètes."""


def _get_client() -> OpenAI:
    return OpenAI(api_key=settings.openai_api_key)


def _call_ai(prompt: str, max_tokens: int = 1500) -> str:
    if not settings.openai_api_key or settings.openai_api_key == "sk-your-key-here":
        return _fallback_response(prompt)

    client = _get_client()
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content


def _fallback_response(prompt: str) -> str:
    """Fallback when no API key is configured."""
    return (
        "**[Mode démo - Configurez OPENAI_API_KEY dans .env pour l'analyse IA complète]**\n\n"
        "L'analyse IA nécessite une clé API OpenAI. En mode démo, voici un résumé type :\n\n"
        "- La consommation annuelle de 6 666 MWh présente un profil industriel typique\n"
        "- La répartition jour/nuit (43%/57%) indique un fonctionnement continu\n"
        "- Le taux de couverture PV de 14% offre un potentiel d'optimisation\n"
        "- Recommandation prioritaire : déplacement des horaires de lavage"
    )


def generate_executive_summary(site_data: dict) -> str:
    prompt = f"""Génère une synthèse exécutive (3 paragraphes) pour le rapport d'audit énergétique du site suivant :

Site : {site_data.get('name', 'Usine Bel Algérie')}
Consommation annuelle : {site_data.get('annual_consumption_mwh', 6666)} MWh
Répartition : TGBT1 40%, TGBT2 41%, TGBT3 19%
Tarification : HTA 41 (Pointe: 8.72, Pleine: 1.94, Creuse: 1.02 DZD/kWh)
Facture annuelle : 25 755 833 DZD
Production PV proposée : 828 MWh/an (taux couverture 14%)
Économies potentielles : 1 971 673 DZD/an
CO2 évité : 359 tonnes/an

Structure : contexte, constats principaux, recommandations clés."""
    return _call_ai(prompt)


def generate_consumption_analysis(tgbt_data: list) -> str:
    tgbt_text = "\n".join([
        f"- {t['name']}: Smoy={t['s_moy_kva']}kVA, Smax={t['s_max_kva']}kVA, "
        f"TC={t['tc_pct']}%, cos φ={t['cos_phi']}, part={t['share_pct']}%"
        for t in tgbt_data
    ])
    prompt = f"""Analyse la consommation électrique par TGBT pour un rapport d'audit :

{tgbt_text}

Ventilation jour/nuit : 43%/57%
Consommation weekend : ~500 kW (groupes froids)
Période enregistrée : 344 MWh sur 18 jours

Pour chaque TGBT : constats sur le taux de charge, le cos phi, les tendances.
Conclus sur la répartition globale et les points d'attention."""
    return _call_ai(prompt, 2000)


def generate_recommendations(data: dict) -> str:
    prompt = f"""Génère des recommandations d'économies d'énergie pour ce site industriel :

Consommation annuelle : {data.get('annual_consumption_mwh', 6666)} MWh
Facture : {data.get('cost_dzd', 25_755_833)} DZD/an
Pointe = 14% conso mais 46% facture
Weekend baseline : 500 kW (groupes froids)
Lavage machines : lundi 23:30, jeudi 09:00

Actions identifiées :
- Déplacement horaires lavage → jusqu'à 1 207 059 DZD/an
- Pilotage charges heures pointe → 818 453 DZD/an
- Optimisation groupe froid → 91 405 DZD/an

Classe les recommandations par priorité avec ROI estimé."""
    return _call_ai(prompt, 2000)


def generate_pv_assessment(pv_data: dict) -> str:
    prompt = f"""Évalue le dimensionnement photovoltaïque suivant :

Installation : {pv_data.get('capacity_kwc', 632)} kWc, {pv_data.get('panel_count', 1160)} panneaux
Type : {pv_data.get('panel_type', 'Jinko 545 Tiger Pro 72HC')}
Production annuelle : {pv_data.get('annual_production_mwh', 828)} MWh
Taux de couverture : {pv_data.get('coverage_rate_pct', 14)}%
Rendement spécifique : {pv_data.get('specific_yield_kwh_kwc', 1310)} kWh/kWc
Investissement : {pv_data.get('investment_dzd', 79_500_000)} DZD
ROI : {pv_data.get('roi_years', 15)} ans, TRI : {pv_data.get('tri_pct', 3)}%
CO2 évité : {pv_data.get('co2_avoided_tonnes_year', 359)} tonnes/an

Évalue la pertinence, les points forts et les risques."""
    return _call_ai(prompt)


def generate_chat_response(question: str, site_context: dict) -> str:
    prompt = f"""Contexte du site :
- Site : {site_context.get('name', 'Usine Bel Algérie, Kolea')}
- Consommation : {site_context.get('annual_consumption_mwh', 6666)} MWh/an
- 3 TGBT (40%/41%/19%), tarif HTA 41
- PV : 632 kWc, 828 MWh/an, couverture 14%

Question de l'utilisateur : {question}

Réponds de manière concise et professionnelle avec des données chiffrées."""
    return _call_ai(prompt, 1000)
