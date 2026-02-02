from pydantic import BaseModel, EmailStr


class SRegisterUserData(BaseModel):
	username: str
	email: EmailStr
	password: str


class SLoginUserData(BaseModel):
	email: EmailStr
	password: str
