import enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class ContentType(enum.IntEnum):
	FILM = 1
	CHAPTER = 2


class Comment(Base):

	__tablename__ = "comments"

	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(ForeignKey("users.id"), nullable=False)
	text = Column(String, nullable=False)
	content_type = Column(Integer, nullable=False)
	content_id = Column(Integer, nullable=False)
	parent_id = Column(Integer, ForeignKey('comments.id'), nullable=True)

	user = relationship("User", back_populates="comments")

	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())
