from app.dao.base import BaseDAO
from app.serials.models import Serial


class SerialDAO(BaseDAO):
	model = Serial
