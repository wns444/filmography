from fastapi import FastAPI

from app.films.router import router as films_router
from app.serials.router import router as serials_router
from app.api.router import router as router_api
app = FastAPI()

app.include_router(films_router)
app.include_router(serials_router)
app.include_router(router_api)


@app.get("/")
def main_page():
	return []
