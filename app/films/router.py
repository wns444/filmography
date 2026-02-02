from fastapi import APIRouter, HTTPException

from app.films.dao import FilmDAO

router = APIRouter(
	prefix="/films",
	tags=["Фильмы"]
)


@router.get("/")
async def get_films():
	films = await FilmDAO.find_all()
	return films


@router.get("/{slug}")
async def get_film(slug: str):
	film = await FilmDAO.find_one_or_none({"slug": slug})
	if not film:
		raise HTTPException(404)
	return film


@router.get("/category/{category}")
async def get_category_film(category: str):
	film = await FilmDAO.find_all({"category": category})
	if not film:
		raise HTTPException(404)
	return film
