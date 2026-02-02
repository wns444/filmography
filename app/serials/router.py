from fastapi import APIRouter, HTTPException

from app.serials.dao import SerialDAO
from app.serials.schemas import SerialS

router = APIRouter(
	prefix="/serials",
	tags=["Сериалы"]
)


@router.get("/")
async def get_serials():
	return await SerialDAO.find_all()


@router.get("/{slug}")
async def get_serial(slug: str):
	serial = await SerialDAO.find_one_or_none(**{"slug": slug})
	if not serial:
		raise HTTPException(404)
	return serial


@router.get("/{slug}/{sn}season")
async def get_serial_season(slug: str, sn: int):
	serial = await SerialDAO.find_one_or_none(**{"slug": slug})
	if not serial:
		raise HTTPException(404)
	return serial


@router.post("/")
async def add_serial(serial_data: SerialS):
	await SerialDAO.insert(**serial_data.model_dump())
