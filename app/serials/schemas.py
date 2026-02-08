from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


# Pydantic v2 ORM support
class ConfigModel(BaseModel):
	model_config = {"from_attributes": True}


class SerialChapterS(ConfigModel):
	id: int
	number: int
	name: Optional[str]
	description: Optional[str]
	created_at: Optional[datetime]
	updated_at: Optional[datetime]


class SerialChapterCreate(ConfigModel):
	number: int
	name: Optional[str]
	description: Optional[str]


class SerialChapterUpdate(ConfigModel):
	number: Optional[int]
	name: Optional[str]
	description: Optional[str]


class SerialSeasonS(ConfigModel):
	id: int
	number: int
	name: Optional[str]
	description: Optional[str]
	chapters: Optional[List[SerialChapterS]]
	created_at: Optional[datetime]
	updated_at: Optional[datetime]


class SerialSeasonCreate(ConfigModel):
	number: int
	name: Optional[str]
	description: Optional[str]


class SerialSeasonUpdate(ConfigModel):
	number: Optional[int]
	name: Optional[str]
	description: Optional[str]


class SerialS(ConfigModel):
	slug: str
	name: str
	description: Optional[str]
	rating: float
	category: str


class SerialCreate(ConfigModel):
	slug: str
	name: str
	description: Optional[str]
	rating: float
	category: str


class SerialUpdate(ConfigModel):
	name: Optional[str]
	description: Optional[str]
	rating: Optional[float]
	category: Optional[str]


class SerialOut(SerialS):
	id: int
	seasons: Optional[List[SerialSeasonS]]
	created_at: Optional[datetime]
	updated_at: Optional[datetime]
