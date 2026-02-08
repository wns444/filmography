from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


# Pydantic v2: allow creating models from ORM objects
class ConfigModel(BaseModel):
	model_config = {"from_attributes": True}


class FilmS(ConfigModel):
	slug: str
	name: str
	description: Optional[str]
	rating: float
	category: str


class FilmCreate(ConfigModel):
	slug: str
	name: str
	description: Optional[str]
	rating: float
	category: str


class FilmUpdate(ConfigModel):
	name: Optional[str]
	description: Optional[str]
	rating: Optional[float]
	category: Optional[str]


class FilmOut(FilmS):
	id: int
	created_at: Optional[datetime]
	updated_at: Optional[datetime]


class SearchFilmS(ConfigModel):
	name: Optional[str]
	rating: Optional[float]
	category: Optional[List[str]]
