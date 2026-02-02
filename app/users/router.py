from fastapi import APIRouter, HTTPException
from app.users.auth import get_password_hash, verify_password
from app.users.dao import UserDAO
from app.users.schemas import SUserData

router = APIRouter(
	prefix='/auth',
	tags=["Auth"]
)


@router.post("/register")
async def register_user(user_data: SUserData):
	existing_user = await UserDAO.find_one_or_none({"email": user_data.email})
	if existing_user:
		raise HTTPException(500)
	hashed_password = get_password_hash(user_data.password)
	await UserDAO.insert()


@router.post("/login")
async def login_user(user_data: SUserData):
	existing_user = await UserDAO.find_one_or_none({"email": user_data.email})
	if not existing_user:
		raise HTTPException(500)
