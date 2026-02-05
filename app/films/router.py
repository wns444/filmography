from typing import Optional
from fastapi import APIRouter, HTTPException

from app.films.dao import FilmDAO
from app.films.schemas import FilmS

router = APIRouter(
	prefix="/films",
	tags=["Фильмы"]
)


@router.get("/")
async def get_films(filters: Optional[FilmS] = None):
	filter_params = filters.model_dump(exclude_none=True) if filters else {}
	return await FilmDAO.find_all(**filter_params)


@router.get("/{slug}")
async def get_film(slug: str):
	film = await FilmDAO.find_one_or_none(slug=slug)
	if not film:
		raise HTTPException(404)
	return film
