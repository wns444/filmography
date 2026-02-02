

from sqlalchemy import Column, Integer, String

from app.database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String)
	email = Column(String)
	hashed_password = Column(String)
