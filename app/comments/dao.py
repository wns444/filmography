from app.comments.models import Comment
from app.dao.base import BaseDAO


class CommentDAO(BaseDAO):
	model = Comment
