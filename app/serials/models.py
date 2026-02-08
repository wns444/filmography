from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Serial(Base):

	__tablename__ = "serials"

	id = Column(Integer, primary_key=True, autoincrement=True)
	slug = Column(String, unique=True, index=True)
	name = Column(String, nullable=False)
	description = Column(String, nullable=True)
	rating = Column(Float)
	category = Column(String, nullable=False)

	seasons = relationship("SerialSeason", back_populates="serial", cascade="all, delete-orphan", lazy="selectin")

	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SerialSeason(Base):
	__tablename__ = "serial_seasons"

	id = Column(Integer, primary_key=True, autoincrement=True)
	serial_id = Column(ForeignKey('serials.id'))
	number = Column(Integer)
	name = Column(String, nullable=True)
	description = Column(String, nullable=True)

	serial = relationship("Serial", back_populates="seasons", lazy="joined")
	chapters = relationship("SerialChapter", back_populates="season", cascade="all, delete-orphan", lazy="selectin")

	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SerialChapter(Base):
	__tablename__ = "serial_chapters"

	id = Column(Integer, primary_key=True, autoincrement=True)
	season_id = Column(ForeignKey('serial_seasons.id'))
	number = Column(Integer)
	name = Column(String, nullable=True)
	description = Column(String, nullable=True)

	season = relationship("SerialSeason", back_populates="chapters", lazy="joined")

	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())
