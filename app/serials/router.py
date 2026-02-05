from typing import Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.serials.dao import SerialDAO
from app.serials.schemas import SerialS

router = APIRouter(
	prefix="/serials",
	tags=["Сериалы"]
)


@router.get("/")
async def get_serials(serial_data: Optional[SerialS] = None):
	filter_params = serial_data.model_dump(exclude_none=True) if serial_data else {}
	return await SerialDAO.find_all(**filter_params)


@router.get("/{slug}")
async def get_serial(slug: str):
	serial = await SerialDAO.find_one_or_none(slug=slug)
	if not serial:
		raise HTTPException(404)
	return serial


@router.get("/{slug}/{sn}season")
async def get_serial_season(slug: str, sn: int):
	serial = await SerialDAO.find_one_or_none(slug=slug)
	if not serial:
		raise HTTPException(404)
	return serial


@router.get("/{slug}/{sn}")
async def redirect_to_season(slug: str, sn: int):
	return RedirectResponse(url=f"/{slug}/{sn}season", status_code=307)
