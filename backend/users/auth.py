from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from pydantic import EmailStr
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from typing import Optional

from backend.config import Config
from backend.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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

	if not verify_password(password, exist_user.hashed_password):
		raise HTTPException(409)

	return exist_user


async def get_current_user(token: str = Depends(oauth2_scheme)):
	try:
		payload = jwt.decode(token, Config.PASS_SECRET_KEY, algorithms=[Config.PASS_ALGORITHM])
		user_id: Optional[int] = payload.get("sub")
		if user_id is None:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
	except Exception:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

	user = await UserDAO.find_one_or_none(id=user_id)
	if not user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
	return user
