from typing import Optional
from pydantic import BaseModel
from datetime import datetime


# Pydantic v2 ORM support
class ConfigModel(BaseModel):
	model_config = {"from_attributes": True}


class CommentS(ConfigModel):
	user_id: int
	text: str
	parent_id: Optional[int] = None


class CommentUpdate(ConfigModel):
	text: Optional[str]
	parent_id: Optional[int]


class CommentOut(ConfigModel):
	id: int
	user_id: int
	text: str
	parent_id: Optional[int]
	content_type: int
	content_id: int
	created_at: Optional[datetime]
	updated_at: Optional[datetime]
