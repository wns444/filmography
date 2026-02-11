from backend.dao.base import BaseDAO
from backend.films.models import Film


class FilmDAO(BaseDAO):
	model = Film
