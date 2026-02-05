from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.sql import func
from app.database import Base


class Film(Base):

	__tablename__ = "films"

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, nullable=False)
	slug = Column(String)
	description = Column(String)
	rating = Column(Float)
	category = Column(String, nullable=False)

	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())
