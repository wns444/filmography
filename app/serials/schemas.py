from typing import Optional
from pydantic import BaseModel


class SerialS(BaseModel):
	slug: str
	name: str
	description: Optional[str]
	rating: float
	category: str
