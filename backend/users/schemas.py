from typing import Optional
from pydantic import BaseModel, EmailStr


class SRegisterUserData(BaseModel):
	username: str
	email: EmailStr
	password: str


class SLoginUserData(BaseModel):
	email: EmailStr
	password: str


class SUsersFilter(BaseModel):
	id: Optional[int]
	username: Optional[str]
	email: Optional[EmailStr]
