from typing import Optional
from pydantic import BaseModel


class CommentS(BaseModel):
	user_id: int
	text: str
	parent_id: Optional[int]
