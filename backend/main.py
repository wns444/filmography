from fastapi import FastAPI

from backend.api.router import router as router_api
from backend.users.router import router as router_user


app = FastAPI()

app.include_router(router_api)
app.include_router(router_user)


@app.get("/")
def main_page():
	return []
