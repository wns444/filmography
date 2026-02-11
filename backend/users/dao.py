from backend.dao.base import BaseDAO
from backend.users.models import User


class UserDAO(BaseDAO):
	model = User
