from typing import List, Optional
from fastapi import APIRouter
from data.constants import SITES, TGBTS
from models.schemas import Site, TGBT

router = APIRouter(prefix="/api/sites", tags=["Sites"])


@router.get("/")
def list_sites() -> List[Site]:
    result = []
    for site_id, site_data in SITES.items():
        tgbts = [TGBT(**t) for t in TGBTS.get(site_id, [])]
        result.append(Site(
            id=site_data["id"],
            name=site_data["name"],
            address=site_data["address"],
            activity=site_data["activity"],
            contract_type=site_data["contract_type"],
            annual_consumption_mwh=site_data["annual_consumption_mwh"],
            subscribed_power_kw=site_data["subscribed_power_kw"],
            tgbts=tgbts,
        ))
    return result


@router.get("/{site_id}")
def get_site(site_id: str) -> Site:
    site_data = SITES[site_id]
    tgbts = [TGBT(**t) for t in TGBTS.get(site_id, [])]
    return Site(
        id=site_data["id"],
        name=site_data["name"],
        address=site_data["address"],
        activity=site_data["activity"],
        contract_type=site_data["contract_type"],
        annual_consumption_mwh=site_data["annual_consumption_mwh"],
        subscribed_power_kw=site_data["subscribed_power_kw"],
        tgbts=tgbts,
    )
