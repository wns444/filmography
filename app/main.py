from fastapi import FastAPI

from app.films.router import router as films_router
from app.serials.router import router as serials_router

app = FastAPI()

app.include_router(films_router)
app.include_router(serials_router)


@app.get("/")
def main_page():
	return []
