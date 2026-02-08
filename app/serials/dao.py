from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.serials.models import Serial, SerialSeason, SerialChapter


class SerialDAO(BaseDAO):
	model = Serial

	@classmethod
	async def find_one_with_relations(cls, **filters):
		async with cls._get_session() as session:
			query = select(cls.model).options(
				selectinload(Serial.seasons).selectinload(SerialSeason.chapters)
			).filter_by(**filters)
			result = await session.execute(query)
			return result.scalar_one_or_none()

	# helper to reuse session creation if needed elsewhere
	@classmethod
	def _get_session(cls):
		from app.database import async_session_maker

		return async_session_maker()


class SerialSeasonDAO(BaseDAO):
	model = SerialSeason


class SerialChapterDAO(BaseDAO):
	model = SerialChapter
