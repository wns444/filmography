from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Film(Base):

	__tablename__ = "films"

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, nullable=False)
	slug = Column(String)
	description = Column(String)
	rating = Column(Float)
	category = Column(String, nullable=False)
