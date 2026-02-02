from app.dao.base import BaseDAO
from app.films.models import Film


class FilmDAO(BaseDAO):
	model = Film
