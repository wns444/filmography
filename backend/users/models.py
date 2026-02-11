from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String)
	email = Column(String)
	hashed_password = Column(String)

	is_veryfied_email = Column(Boolean, nullable=False, default=False)

	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())

	comments = relationship("Comment", back_populates="user")
