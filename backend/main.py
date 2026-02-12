from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import router as router_api
from backend.users.router import router as router_user


app = FastAPI()

app.include_router(router_api)
app.include_router(router_user)

origins = [
	"http://localhost:3000",
	"http://0.0.0.0:3000",
	"http://127.0.0.1:3000",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/")
def main_page():
	return []
