from typing import Optional
from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.films.dao import FilmDAO
from app.films.schemas import SearchFilmS, FilmCreate, FilmUpdate, FilmOut
from app.serials.dao import SerialDAO
from app.serials.schemas import SerialS, SerialOut, SerialCreate, SerialUpdate
from app.serials.schemas import (
	SerialSeasonCreate,
	SerialSeasonUpdate,
	SerialChapterCreate,
	SerialChapterUpdate,
	SerialSeasonS,
	SerialChapterS,
)
from app.serials.dao import SerialSeasonDAO, SerialChapterDAO
from app.comments.dao import CommentDAO
from app.comments.models import ContentType
from app.comments.schemas import CommentS, CommentUpdate, CommentOut
from app.api.deps import get_current_user


router = APIRouter(prefix="/api/v1", tags=["API"])


# Films


@router.get("/films/", response_model=list[FilmOut])
async def get_films(filters: Optional[SearchFilmS] = None, limit: int = 100, offset: int = 0):
	filter_params = filters.model_dump(exclude_none=True) if filters else {}
	return await FilmDAO.find_all(filters=filter_params, limit=limit, offset=offset)


@router.get("/films/{slug}", response_model=FilmOut)
async def get_film(slug: str):
	film = await FilmDAO.find_one_or_none(slug=slug)
	if not film:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
	return film


@router.post("/films/", response_model=FilmOut, status_code=status.HTTP_201_CREATED)
async def create_film(payload: FilmCreate):
	data = payload.model_dump()
	created = await FilmDAO.create(**data)
	return created


@router.put("/films/{slug}", response_model=FilmOut)
async def update_film(slug: str, payload: FilmUpdate):
	film = await FilmDAO.find_one_or_none(slug=slug)
	if not film:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
	data = payload.model_dump(exclude_none=True)
	updated = await FilmDAO.update(filters={"slug": slug}, **data)
	return updated


@router.delete("/films/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_film(slug: str):
	ok = await FilmDAO.delete(slug=slug)
	if not ok:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
	return None

# Comments (film comments)


@router.get("/films/{id}/comments", response_model=list[CommentOut])
async def get_film_comments(id: int):
	return await CommentDAO.get_all_comments(
		content_type=ContentType.FILM,
		content_id=id,
	)


@router.post("/films/{id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def add_comment(id: int, comment: CommentS, user=Depends(get_current_user)):
	data = comment.model_dump()
	data["user_id"] = user.id
	created = await CommentDAO.create(content_type=ContentType.FILM, content_id=id, **data)
	return created


# Serials


@router.get("/serials/", response_model=list[SerialOut])
async def get_serials(serial_data: Optional[SerialS] = None, limit: int = 100, offset: int = 0):
	filter_params = serial_data.model_dump(exclude_none=True) if serial_data else {}
	return await SerialDAO.find_all(filters=filter_params, limit=limit, offset=offset)


@router.get("/serials/{slug}", response_model=SerialOut)
async def get_serial(slug: str):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	return serial


@router.get("/serials/{slug}/seasons/", response_model=list[SerialSeasonS])
async def list_seasons(slug: str):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	return serial.seasons or []


@router.get("/serials/{slug}/seasons/{sn}", response_model=SerialSeasonS)
async def get_serial_season(slug: str, sn: int):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	season = next((s for s in serial.seasons if s.number == sn), None)
	if not season:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	return season


@router.post("/serials/", response_model=SerialOut, status_code=status.HTTP_201_CREATED)
async def create_serial(payload: SerialCreate):
	data = payload.model_dump()
	created = await SerialDAO.create(**data)
	return created


@router.put("/serials/{slug}", response_model=SerialOut)
async def update_serial(slug: str, payload: SerialUpdate):
	serial = await SerialDAO.find_one_or_none(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	data = payload.model_dump(exclude_none=True)
	updated = await SerialDAO.update(filters={"slug": slug}, **data)
	return updated


@router.delete("/serials/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_serial(slug: str):
	ok = await SerialDAO.delete(slug=slug)
	if not ok:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	return None



# Seasons CRUD


@router.post("/serials/{slug}/seasons/", status_code=status.HTTP_201_CREATED, response_model=SerialSeasonS)
async def create_season(slug: str, payload: SerialSeasonCreate):
	serial = await SerialDAO.find_one_or_none(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	data = payload.model_dump()
	data["serial_id"] = serial.id
	created = await SerialSeasonDAO.create(**data)
	return created


@router.put("/serials/{slug}/seasons/{sn}", response_model=SerialSeasonS)
async def update_season(slug: str, sn: int, payload: SerialSeasonUpdate):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	season = next((s for s in serial.seasons if s.number == sn), None)
	if not season:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	data = payload.model_dump(exclude_none=True)
	updated = await SerialSeasonDAO.update(obj_id=season.id, **data)
	return updated


@router.delete("/serials/{slug}/seasons/{sn}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_season(slug: str, sn: int):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	season = next((s for s in serial.seasons if s.number == sn), None)
	if not season:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	ok = await SerialSeasonDAO.delete(obj_id=season.id)
	if not ok:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	return None


# Chapters CRUD


@router.post("/serials/{slug}/seasons/{sn}/chapters/", status_code=status.HTTP_201_CREATED, response_model=SerialChapterS)
async def create_chapter(slug: str, sn: int, payload: SerialChapterCreate):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	season = next((s for s in serial.seasons if s.number == sn), None)
	if not season:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	data = payload.model_dump()
	data["season_id"] = season.id
	created = await SerialChapterDAO.create(**data)
	return created


@router.get("/serials/{slug}/seasons/{sn}/chapters/", response_model=list[SerialChapterS])
async def list_chapters(slug: str, sn: int):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	season = next((s for s in serial.seasons if s.number == sn), None)
	if not season:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	return season.chapters or []


@router.get("/serials/{slug}/seasons/{sn}/chapters/{cn}", response_model=SerialChapterS)
async def get_chapter(slug: str, sn: int, cn: int):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	season = next((s for s in serial.seasons if s.number == sn), None)
	if not season:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	chapter = next((c for c in season.chapters if c.number == cn), None)
	if not chapter:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
	return chapter


@router.put("/serials/{slug}/seasons/{sn}/chapters/{cn}", response_model=SerialChapterS)
async def update_chapter(slug: str, sn: int, cn: int, payload: SerialChapterUpdate):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	season = next((s for s in serial.seasons if s.number == sn), None)
	if not season:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	chapter = next((c for c in season.chapters if c.number == cn), None)
	if not chapter:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
	data = payload.model_dump(exclude_none=True)
	updated = await SerialChapterDAO.update(obj_id=chapter.id, **data)
	return updated


@router.delete("/serials/{slug}/seasons/{sn}/chapters/{cn}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chapter(slug: str, sn: int, cn: int):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	season = next((s for s in serial.seasons if s.number == sn), None)
	if not season:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	chapter = next((c for c in season.chapters if c.number == cn), None)
	if not chapter:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
	ok = await SerialChapterDAO.delete(obj_id=chapter.id)
	if not ok:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
	return None

# Comments for serial chapters


@router.get("/serials/{slug}/seasons/{sn}/chapters/{cn}/comments", response_model=list[CommentOut])
async def get_chapter_comments(slug: str, sn: int, cn: int):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	season = next((s for s in serial.seasons if s.number == sn), None)
	if not season:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	chapter = next((c for c in season.chapters if c.number == cn), None)
	if not chapter:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
	return await CommentDAO.get_all_comments(content_type=ContentType.CHAPTER, content_id=chapter.id)


@router.post("/serials/{slug}/seasons/{sn}/chapters/{cn}/comments", status_code=status.HTTP_201_CREATED, response_model=CommentOut)
async def add_chapter_comment(slug: str, sn: int, cn: int, comment: CommentS, user=Depends(get_current_user)):
	serial = await SerialDAO.find_one_with_relations(slug=slug)
	if not serial:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serial not found")
	season = next((s for s in serial.seasons if s.number == sn), None)
	if not season:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
	chapter = next((c for c in season.chapters if c.number == cn), None)
	if not chapter:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
	data = comment.model_dump()
	data["user_id"] = user.id
	created = await CommentDAO.create(content_type=ContentType.CHAPTER, content_id=chapter.id, **data)
	return created


# Comment update/delete


@router.put("/comments/{comment_id}")
async def update_comment(comment_id: int, payload: CommentUpdate, user=Depends(get_current_user)):
	existing = await CommentDAO.get(comment_id)
	if not existing:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
	if existing.user_id != user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to modify this comment")
	data = payload.model_dump(exclude_none=True)
	updated = await CommentDAO.update(obj_id=comment_id, **data)
	if not updated:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
	return updated


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, user=Depends(get_current_user)):
	existing = await CommentDAO.get(comment_id)
	if not existing:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
	if existing.user_id != user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to delete this comment")
	ok = await CommentDAO.delete(obj_id=comment_id)
	if not ok:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
	return None
