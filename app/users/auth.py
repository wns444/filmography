from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from pydantic import EmailStr

from app.config import Config
from app.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
	to_encode = data.copy()
	expire = datetime.now(timezone.utc) + timedelta(minutes=30)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(
		to_encode, Config.PASS_SECRET_KEY, Config.PASS_ALGORITHM
	)
	return encoded_jwt


async def auth_user(email: EmailStr, password: str) -> str:
	exist_user = await UserDAO.find_one_or_none(email=email)

	if not exist_user:
		raise HTTPException(500)

	if not verify_password(password, get_password_hash(exist_user.hashed_password)):
		raise HTTPException(409)

	return exist_user
