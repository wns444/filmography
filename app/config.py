import os
import dotenv

dotenv.load_dotenv()


class Config:
	DB_USER: str = os.getenv("DB_USER")
	DB_PASS: str = os.getenv("DB_PASS")
	DB_HOST: str = os.getenv("DB_HOST")
	DB_PORT: str = os.getenv("DB_PORT")
	DB_NAME: str = os.getenv("DB_NAME")

	@classmethod
	def get_database_url(cls):
		return f"postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASS}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

	PASS_SECRET_KEY: str = os.getenv("PASS_SECRET_KEY")
	PASS_ALGORITHM: str = os.getenv("PASS_ALGORITHM")
