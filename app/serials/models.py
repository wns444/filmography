from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
# from slugify import slugify


class Serial(Base):

	__tablename__ = "serials"

	id = Column(Integer, primary_key=True, autoincrement=True)
	slug = Column(String)
	name = Column(String, nullable=False)
	description = Column(String, nullable=True)
	rating = Column(Float)
	category = Column(String, nullable=False)
	seasons = relationship("SerialSeason", back_populates="season")


class SerialSeason(Base):
	__tablename__ = "serial_seasons"

	id = Column(Integer, primary_key=True, autoincrement=True)
	serial_id = Column(ForeignKey('serials.id'))
	number = Column(Integer)
	name = Column(String, nullable=True)
	description = Column(String, nullable=True)

	season = relationship("Serial", back_populates="seasons")
	chapters = relationship("SerialChapter", back_populates="chapter")


class SerialChapter(Base):
	__tablename__ = "serial_chapters"

	id = Column(Integer, primary_key=True, autoincrement=True)
	season_id = Column(ForeignKey('serial_seasons.id'))
	number = Column(Integer)
	name = Column(String, nullable=True)
	description = Column(String, nullable=True)

	chapter = relationship("SerialSeason", back_populates="chapters")
