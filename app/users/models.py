from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String)
	email = Column(String)
	hashed_password = Column(String)

	is_veryfied_email = Column(Boolean, nullable=False, default=False)
