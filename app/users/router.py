from fastapi import APIRouter, HTTPException, Response
from app.users.auth import auth_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.schemas import SLoginUserData, SRegisterUserData

router = APIRouter(
	prefix='/auth',
	tags=["Auth"]
)


@router.post("/register")
async def register_user(user_data: SRegisterUserData):
	existing_by_email = await UserDAO.find_one_or_none(email=user_data.email)
	if existing_by_email:
		raise HTTPException(status_code=409, detail="Email already registered")

	existing_by_username = await UserDAO.find_one_or_none(username=user_data.username)
	if existing_by_username:
		raise HTTPException(status_code=409, detail="Username already taken")

	hashed_password = get_password_hash(user_data.password)
	await UserDAO.insert(
		email=user_data.email,
		username=user_data.username,
		hashed_password=hashed_password,
		is_veryfied_email=False
	)


@router.post("/login")
async def login_user(response: Response, user_data: SLoginUserData):
	user = await auth_user(user_data.email, user_data.password)
	access_token = create_access_token(
		{"sub": user.id}
	)
	response.set_cookie(
		"filmography_token", access_token, httponly=True
	)
