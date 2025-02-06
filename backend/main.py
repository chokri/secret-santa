import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.santa.routes import router as santa_toutes
from modules.users.routes import router as users_routes
from starlette.datastructures import CommaSeparatedStrings

stage = os.environ.get('STAGE', None)
ALLOWED_HOSTS=CommaSeparatedStrings(os.environ.get('ALLOWED_HOSTS', ''))

app = FastAPI(
    title="Secret Santa API",
    description="Backend API fro Secret Santa Application",
    root_path=f"/{stage}" if stage else "/",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_routes, prefix="/api")
app.include_router(santa_toutes, prefix="/api")
