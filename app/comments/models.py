from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Comment(Base):

	__tablename__ = "comments"

	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(ForeignKey("users.id"), nullable=False)
	text = Column(String, nullable=False)
	parent_id = Column(Integer, ForeignKey('comments.id'), nullable=True)

	children = relationship("Comment", backref="parent", remote_side=[id])
	user = relationship("User", back_populates="users")

	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())
