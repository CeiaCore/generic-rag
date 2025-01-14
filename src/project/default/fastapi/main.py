
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.project.default.fastapi.routes.chat_router import chat_router

app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost.tiangolo.com",
    "http://200.137.197.240",
    "https://200.137.197.240",
    "https://mraristotle.site",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router, prefix="/api/v1/chat_router")

