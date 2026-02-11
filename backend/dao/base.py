from typing import Any, Dict, List, Optional
from sqlalchemy import select

from backend.database import async_session_maker


class BaseDAO:
	model = None

	@classmethod
	async def get(cls, obj_id: int):
		async with async_session_maker() as session:
			query = select(cls.model).filter_by(id=obj_id)
			result = await session.execute(query)
			return result.scalar_one_or_none()

	@classmethod
	async def find_one_or_none(cls, **filters) -> Optional[model]:
		async with async_session_maker() as session:
			query = select(cls.model).filter_by(**filters)
			result = await session.execute(query)
			return result.scalar_one_or_none()

	@classmethod
	async def find_all(cls, filters: Optional[Dict[str, Any]] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[model]:
		filters = filters or {}
		async with async_session_maker() as session:
			query = select(cls.model).filter_by(**filters)
			if limit is not None:
				query = query.limit(limit)
			if offset is not None:
				query = query.offset(offset)
			all_results = await session.execute(query)
			return all_results.scalars().all()

	@classmethod
	async def create(cls, **data) -> model:
		async with async_session_maker() as session:
			obj = cls.model(**data)
			session.add(obj)
			await session.commit()
			await session.refresh(obj)
			return obj

	@classmethod
	async def update(cls, obj_id: Optional[int] = None, filters: Optional[Dict[str, Any]] = None, **data) -> Optional[model]:
		async with async_session_maker() as session:
			if obj_id is not None:
				query = select(cls.model).filter_by(id=obj_id)
			elif filters:
				query = select(cls.model).filter_by(**filters)
			else:
				raise ValueError("Provide obj_id or filters to update")

			result = await session.execute(query)
			obj = result.scalar_one_or_none()
			if not obj:
				return None
			for key, value in data.items():
				setattr(obj, key, value)
			session.add(obj)
			await session.commit()
			await session.refresh(obj)
			return obj

	@classmethod
	async def delete(cls, obj_id: Optional[int] = None, **filters) -> bool:
		async with async_session_maker() as session:
			if obj_id is not None:
				query = select(cls.model).filter_by(id=obj_id)
			elif filters:
				query = select(cls.model).filter_by(**filters)
			else:
				raise ValueError("Provide obj_id or filters to delete")

			result = await session.execute(query)
			obj = result.scalar_one_or_none()
			if not obj:
				return False
			await session.delete(obj)
			await session.commit()
			return True
