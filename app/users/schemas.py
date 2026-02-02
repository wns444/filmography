from pydantic import BaseModel, EmailStr


class SUserData(BaseModel):
	username: str
	email: EmailStr
	password: str
