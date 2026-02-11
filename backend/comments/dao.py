from typing import Union

from sqlalchemy import select
from backend.comments.models import Comment, ContentType
from backend.dao.base import BaseDAO
from backend.database import async_session_maker
from backend.users.models import User


class CommentDAO(BaseDAO):
	model = Comment

	@classmethod
	async def get_all_comments(cls, content_type: Union[ContentType.FILM, ContentType.CHAPTER], content_id: int):
		async with async_session_maker() as session:
			query = (
				select(cls.model, User.username, User.email)
				.where(
					cls.model.content_type == content_type,
					cls.model.content_id == content_id
				)
				.join(User, cls.model.user_id == User.id)
			)
			result = await session.execute(query)
			comments_with_user = []
			for comment, username, email in result:
				comment.user_info = {"username": username, "email": email}  # Добавляем как атрибут
				comments_with_user.append(comment)

			return comments_with_user
