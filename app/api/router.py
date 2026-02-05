from typing import Optional
from fastapi import APIRouter

from app.comments.dao import CommentDAO
from app.comments.schemas import CommentS
from app.films.dao import FilmDAO
from app.films.schemas import FilmS
from app.serials.dao import SerialDAO
from app.serials.schemas import SerialS
from app.users.dao import UserDAO
from app.users.schemas import SUsersFilter

router = APIRouter(
	prefix="/api/v1",
	tags=["API"]
)

router_add = APIRouter(
	prefix="/add"
)

router_del = APIRouter(
	prefix="/delete"
)


@router.get("/users")
async def get_users(users_filters: Optional[SUsersFilter] = None):
	filter_params = users_filters.model_dump(exclude_none=True) if users_filters else {}
	return await UserDAO.find_all(**filter_params)


# ADD ROUTES
@router_add.post("/serial")
async def add_serial(serial_data: SerialS):
	await SerialDAO.insert(**serial_data.model_dump())


@router_add.post("/film")
async def add_film(serial_data: FilmS):
	await FilmDAO.insert(**serial_data.model_dump())


@router_add.post("/comment")
async def add_comment(comment: CommentS):
	return await CommentDAO.insert(**comment)


# DELETE ROUTES
@router_del.delete("/serial")
async def del_serial(serial_data: SerialS):
	await SerialDAO.insert(**serial_data.model_dump())


@router_del.delete("/film")
async def del_film(serial_data: FilmS):
	await SerialDAO.insert(**serial_data.model_dump())


@router_del.delete("/user")
async def del_user(users_filters: SUsersFilter = None):
	filter_params = users_filters.model_dump(exclude_none=True) if users_filters else {}
	return await UserDAO.find_all(**filter_params)


router.include_router(router_add)
router.include_router(router_del)
